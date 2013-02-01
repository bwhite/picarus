
"""
Changed w/ Andrew - Dec 16
- Update mfeat and mask column families to use compression
- Setup new mfeat to work on logos
- Double check that the ILP is being used properly for the masks
- Add mask indexing
- Add thumbnail creation for image search to Preprocessor
- Add logo images to database
- Add live camera images to database
- Update camera/live demos to use the standard /data/ paths instead of custom methods
- Update classifier_explorer confs to pull from hbase
- Update login to use new .js library
- Everything is verb based (e.g., /see/scene) with input specified in as parameters
-- Single Image Input: 1.) param['image_b64'], 2.) file['image'], 3.) param['image_url'], or 4.) param['image_path']
-- Image path: /data/images/brandyn/image_small

Not sure yet
- Upload image temporarily and then resize/preprocess
- Creation of verb on the fly for streaming tasks (online classifier, background subtraction, common operations)

/data/
/data/<table>/*/<col>?op=see/scene/indoor&input=//<in_col>
/data/<table>/*/<col>?op=scene/indoor&input=<out_table>/*/<out_col>
/data/<table>/<row>/<col>?vision=scene/indoor&input=<out_table>/<out_row>/<out_col>


/data/<table>/<col>?vision=scene/indoor

/see/
/see/search/logo
/see/detect/
/see/classify/scene
/see/segment/texton
/see/segment/texton/argmax
/see/feature/gist
/see/points/surf
/learn/cluster/kmeans
/learn/classifier/svm
"""
from gevent import monkey
monkey.patch_all()
import json
import mimerender
import bottle
import os
import argparse
import random
import base64
import imfeat
import time
import redis
import hadoopy_hbase
import cPickle as pickle
import numpy as np
import cv2
import gevent
import crawlers
import hashlib
import multiprocessing
import distpy
from users import Users, UnknownUser
from picarus.modules import HashRetrievalClassifier
import picarus._features
import boto
from picarus._importer import call_import
from driver import PicarusManager
import logging
import uuid
import contextlib
logging.basicConfig(level=logging.DEBUG)
bottle.debug(True)

VERSION = 'a1'


def check_version(func):

    def inner(version, *args, **kw):
        if version != VERSION:
            bottle.abort(400)
        return func(*args, **kw)
    return inner

if __name__ == "__main__":
    mimerender = mimerender.BottleMimeRender()
    render_xml = lambda message: '<message>%s</message>'%message
    render_json = lambda **args: json.dumps(args)
    render_html = lambda message: '<html><body>%s</body></html>'%message
    render_txt = lambda message: message
    render_xml_exception = lambda exception: '<exception>%s</exception>' % exception.message
    render_json_exception = lambda exception: json.dumps({'exception': exception.message})

    parser = argparse.ArgumentParser(description='Run Picarus REST Frontend')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=6380)
    parser.add_argument('--redis_db', type=int, help='Redis DB', default=0)
    parser.add_argument('--port', default='15000', type=int)
    parser.add_argument('--thrift_server', default='localhost')
    parser.add_argument('--thrift_port', default='9090')
    ARGS = parser.parse_args()
    THRIFT = hadoopy_hbase.connect(ARGS.thrift_server, ARGS.thrift_port)
    THRIFT_LOCK = gevent.coros.RLock()
    USERS = Users(ARGS.redis_host, ARGS.redis_port, ARGS.redis_db)
    MANAGER = PicarusManager(thrift=THRIFT)


@contextlib.contextmanager
def thrift_lock():
    try:
        THRIFT_LOCK.acquire()
        yield THRIFT
    finally:
        THRIFT_LOCK.release()


def print_request():
    ks = ['auth', 'content_length', 'content_type', 'environ', 'fullpath', 'is_ajax', 'is_xhr', 'method', 'path', 'query_string', 'remote_addr', 'remote_route', 'script_name', 'url', 'urlparts']
    for k in ks:
        print('%s: %s' % (k, str(getattr(bottle.request, k))))

    print('%s: %s' % ('files', (getattr(bottle.request, 'files')).keys()))

    ks = ['forms', 'params', 'query', 'cookies', 'headers']
    for k in ks:
        print('%s: %s' % (k, str(dict(getattr(bottle.request, k)))))


@bottle.get('/<version:re:[^/]*>/user')
@USERS.auth(True)
@check_version
def user_info(auth_user):
    print(auth_user.user)
    return {'stats': auth_user.stats(), 'uploadRowPrefix': auth_user.upload_row_prefix}


@bottle.post('/<version:re:[^/]*>/data/<table:re:[^/]+>')
@USERS.auth(True)
@check_version
def data_row_upload(auth_user, table):
    with thrift_lock() as thrift:
        prefix = auth_user.upload_row_prefix
        row = prefix + '%.10d%s' % (2147483648 - int(time.time()), uuid.uuid4().bytes)
        mutations = []
        # TODO: Reuse PATCH code which also does this
        for x in bottle.request.files:
            thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=bottle.request.files[x].file.read())])
        for x in set(bottle.request.params) - set(bottle.request.files):
            mutations.append(hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=bottle.request.params[x]))
        if mutations:
            thrift.mutateRow(table, row, mutations)
        return {'row': base64.urlsafe_b64encode(row)}


@bottle.route('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>', 'PATCH')
@bottle.post('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@bottle.delete('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@bottle.get('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@USERS.auth()
@check_version
def data_row(table, row):
    with thrift_lock() as thrift:
        row = base64.urlsafe_b64decode(row)
        method = bottle.request.method.upper()
        # TODO Check authentication per table
        if not (table and row):
            bottle.abort(400)
        if table not in ('images'):
            bottle.abort(400)
        if method == 'GET':
            columns = sorted(bottle.request.params.getall('column'))
            if columns:
                result = thrift.getRowWithColumns(table, row, columns)
            else:
                result = thrift.getRow(table, row)
            if not result:
                bottle.abort(404)
            return {base64.urlsafe_b64encode(x): base64.b64encode(y.value)
                    for x, y in result[0].columns.items()}
        elif method == 'PATCH':
            mutations = []
            for x in bottle.request.files:
                thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=x, value=bottle.request.files[x].file.read())])
            for x in set(bottle.request.params) - set(bottle.request.files):
                mutations.append(hadoopy_hbase.Mutation(column=x, value=bottle.request.params[x]))
            if mutations:
                thrift.mutateRow(table, row, mutations)
            return {}
        elif method == 'POST':
            action = bottle.request.params['action']
            if action == 'i/classify':
                image_column = base64.urlsafe_b64decode(bottle.request.params['imageColumn'])
                results = thrift.get(table, row, image_column)
                if not results:
                    print((table, row, image_column))
                    bottle.abort(404)
                classifier = _classifier_from_key(base64.urlsafe_b64decode(bottle.request.params['model']))
                return json.dumps(classifier(results[0].value))
            else:
                bottle.abort(400)
        elif method == 'DELETE':
            thrift.deleteAllRow(table, row)
            return {}
        else:
            bottle.abort(400)


@bottle.delete('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>/<col:re:[^/]+>')
def data_row_col(table, row, col):
    with thrift_lock() as thrift:
        row = base64.urlsafe_b64decode(row)
        col = base64.urlsafe_b64decode(col)
        if table not in ('images'):
            bottle.abort(400)
        thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=col, isDelete=True)])
        return {}


SCANNER_CACHE = {}  # [(start_row, end_row, col, max_rows, cursor)]


def _get_cached_scanner(start_row, stop_row, cols, max_rows, exclude_start):
    cols = tuple(cols)
    if not exclude_start:
        raise KeyError
    cursor = bottle.request.params['cursor']
    scanner_key = (start_row, stop_row, cols, max_rows, cursor)
    scanner = SCANNER_CACHE[scanner_key]
    print('Reusing cached scanner [%s]' % str(scanner_key))
    del SCANNER_CACHE[scanner_key]
    return scanner


@bottle.get('/<version:re:[^/]*>/slice/<table:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>')
@USERS.auth()
@check_version
def data_rows(table, start_row, stop_row):
    with thrift_lock() as thrift:
        start_row = base64.urlsafe_b64decode(start_row)
        stop_row = base64.urlsafe_b64decode(stop_row)
        method = bottle.request.method.upper()
        columns = map(base64.urlsafe_b64decode, sorted(bottle.request.params.getall('column')))
        # TODO Check authentication per table
        if table not in ('images',):
            raise ValueError('Only images allowed for now!')
        if method == 'GET':
            # TODO: Need to verify limits on this scan and check auth
            max_rows = min(101, int(bottle.request.params.get('maxRows', 1)))
            exclude_start = bool(int(bottle.request.params.get('excludeStart', 0)))
            try:
                scanner = _get_cached_scanner(start_row, stop_row, columns, max_rows, exclude_start)
                exclude_start = False
            except KeyError:
                scanner = hadoopy_hbase.scanner(thrift, table, columns=columns,
                                                start_row=start_row, per_call=max_rows,
                                                stop_row=stop_row)
            stopped_early = False
            out = []
            for row_num, (cur_row, cur_columns) in enumerate(scanner, 1):
                if exclude_start and row_num == 1:
                    continue
                out.append((base64.urlsafe_b64encode(cur_row), {base64.urlsafe_b64encode(k): base64.b64encode(v) for k, v in cur_columns.items()}))
                if row_num >= max_rows:
                    stopped_early = True
                    break
            result_out = {'data': out}
            if stopped_early:
                result_out['cursor'] = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]
                SCANNER_CACHE[(cur_row, stop_row, tuple(columns), max_rows, result_out['cursor'])] = scanner
            return result_out
        else:
            bottle.abort(400)


def _classifier_from_key(key):
    input, classifier, param = MANAGER.key_to_input_model_param(key)
    if param['classifier_type'] == 'sklearn_decision_func':
        real_classifier = lambda x: float(classifier.decision_function(x).flat[0])
    else:
        real_classifier = classifier
    input, feature, param = MANAGER.key_to_input_model_param(input['feature'])
    loader = lambda x: call_import(x) if isinstance(x, dict) else x
    feature = loader(feature)
    if param['feature_type'] == 'multi_feature':
        real_feature = lambda x: feature.compute_dense(x)
    else:
        real_feature = feature
    input, preprocessor, param = MANAGER.key_to_input_model_param(input['image'])
    preprocessor = loader(preprocessor)
    return lambda x: real_classifier(real_feature(preprocessor.asarray(x)))


def _get_texton():
    forests = []
    threshs = [0.]
    for x in ['outdoor', 'indoor']:
        tp = pickle.load(open('tree_ser-%s-texton.pkl' % x))
        tp2 = pickle.load(open('tree_ser-%s-integral.pkl' % x))
        forests.append({'tp': tp, 'tp2': tp2})
    return picarus._features.TextonILPPredict(num_classes=8, ilp=MANAGER.key_to_classifier_pb('pred:h\x90\xf57\\\x8az\x0f\xd0K\xb6\xbc\xd7\taG\xa61l\x9b').SerializeToString(),
                                              forests=forests, threshs=threshs)


@bottle.post('/<version:re:[^/]*>/image')
@USERS.auth()
@check_version
def image():
    image = imfeat.image_fromstring(bottle.request.files['image'].file.read())
    image = imfeat.resize_image_max_side(image, 320)
    image_string = imfeat.image_tostring(image, 'jpg')
    return {'jpgb64': base64.b64encode(image_string)}


@bottle.route('/<version:re:[^/]*>/models/<row:re:[^/]+>', 'PATCH')
@bottle.put('/<version:re:[^/]*>/models/<row:re:[^/]+>')
@USERS.auth()
@check_version
def models_update(row):
    try:
        THRIFT_LOCK.acquire()
        data = bottle.request.json
        kvs = {}
        print(data)
        try:
            kvs['data:notes'] = data['notes']
        except KeyError:
            pass
        try:
            kvs['data:tags'] = data['tags']
        except KeyError:
            pass
        THRIFT.mutateRow('picarus_models', base64.urlsafe_b64decode(row), [hadoopy_hbase.Mutation(column=k, value=v) for k, v in kvs.items()])
    finally:
        THRIFT_LOCK.release()
    return {}


@bottle.delete('/<version:re:[^/]*>/models/<row:re:[^/]+>')
@USERS.auth()
@check_version
def model_delete():
    print_request()


@bottle.get('/<version:re:[^/]*>/models')
@USERS.auth()
@check_version
def models():
    out = []
    prefix_to_name = {'feat:': 'feature',
                      'mfeat:': 'multi-feature',
                      'mask:': 'mask-feature',
                      'pred:': 'classifier',
                      'srch:': 'index',
                      'hash:': 'hasher',
                      'data:': 'preprocessor'}
    try:
        THRIFT_LOCK.acquire()
        for row, cols in hadoopy_hbase.scanner(THRIFT, 'picarus_models', columns=['data:input', 'data:versions', 'data:prefix', 'data:creation_time', 'data:param', 'data:notes', 'data:name', 'data:tags']):
            name = prefix_to_name[cols['data:prefix']]
            out.append({'inputs': json.loads(cols['data:input']),
                        'versions': json.loads(cols['data:versions']),
                        'param': json.loads(cols['data:param']),
                        'creationTime': float(cols['data:creation_time']),
                        'prefix_pretty': name,
                        'notes': cols['data:notes'],
                        'name': cols['data:name'],
                        'tags': cols['data:tags'],
                        'prefix': cols['data:prefix'],
                        'row': base64.urlsafe_b64encode(row)})
    finally:
        THRIFT_LOCK.release()
    return json.dumps(out)


@bottle.get('/static/<name:re:[^/]*>')
def static(name):
    return bottle.static_file(name, root=os.path.join(os.getcwd(), 'static'))


@bottle.post('/<version:re:[^/]*>/user/auth')
@check_version
def auth():
    print_request()
    email = dict(bottle.request.params)['email']
    try:
        USERS.email_auth(email, bottle.request.remote_addr, bottle.request.params['recaptcha_challenge_field'], bottle.request.params['recaptcha_response_field'])
    except UnknownUser:
        bottle.abort(401)
    return 'Emailing auth code'


@bottle.post('/<version:re:[^/]*>/crawl/<crawler:re:[^/]*>')
@check_version
@USERS.auth()
def crawl(crawler):
    print_request()
    row_prefix = bottle.request.params['row_prefix']
    assert row_prefix.find(':') != -1
    class_name = bottle.request.params['class_name']
    query = bottle.request.params.get('query')
    query = class_name if query is None else query
    if crawler == 'flickr':
        p = {}
        p['api_key'] = bottle.request.params['api_key']
        p['api_secret'] = bottle.request.params['api_secret']
        if 'has_geo' in bottle.request.params:
            p['has_geo'] = True
        try:
            p['min_upload_date'] = int(bottle.request.params['min_upload_date'])
        except KeyError:
            pass
        try:
            p['max_upload_date'] = int(bottle.request.params['max_upload_date'])
        except KeyError:
            pass
        try:
            p['page'] = int(bottle.request.params['page'])
        except KeyError:
            pass
        return {'data': {'num_rows': crawlers.flickr_crawl(crawlers.HBaseCrawlerStore(row_prefix), class_name, query, **p)}}
    elif crawler == 'google':
        pass
    else:
        bottle.abort(400)


MTURK_SERVER = None


def _mturk_wrapper(*args, **kw):
    bottle.app[0] = bottle.Bottle()  # Clear previous app
    import mturk_vision
    out = mturk_vision.server(*args, **kw)
    print('Filtering based on annotations')
    MANAGER.filter_annotations_to_hbase()
    return out


@bottle.post('/<version:re:[^/]*>/human/<server_type:re:[^/]*>')
@check_version
@USERS.auth()
def human(server_type):
    global MTURK_SERVER
    assert server_type in ('image_entity', 'image_query')
    assert MTURK_SERVER is None
    secret = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]
    p = {}
    start_row = bottle.request.params['start_row']
    stop_row = bottle.request.params['stop_row']
    image_column = bottle.request.params['image_column']
    if server_type == 'image_entity':
        entity_column = bottle.request.params['entity_column']
        p = {}
        p['data'] = 'hbase://localhost:9090/images/%s/%s?entity=%s&image=%s' % (start_row, stop_row, entity_column, image_column)
        p['type'] = 'image_entity'
    elif server_type == 'image_query':
        query = bottle.request.params['query']
        p['data'] = 'hbase://localhost:9090/images/%s/%s?image=%s' % (start_row, stop_row, image_column)
        p['type'] = 'image_query'
        p['query'] = query
    else:
        bottle.abort(400)
    p['redis_address'] = 'localhost'
    p['redis_port'] = 6382
    p['port'] = 16000
    p['num_tasks'] = 100
    p['mode'] = 'amt'
    p['setup'] = True
    p['reset'] = True
    p['secret'] = secret
    print(p)
    base_url = 'http://api0.picar.us:%d' % p['port']
    admin_prefix = '/admin/%s/' % secret
    MTURK_SERVER = multiprocessing.Process(target=_mturk_wrapper, kwargs=p)
    MTURK_SERVER.start()
    return {'worker': base_url, 'stop': base_url + admin_prefix + 'stop', 'results': base_url + admin_prefix + 'results.js', 'users': base_url + admin_prefix + 'users.js'}


@bottle.post('/<version:re:[^/]*>/dedupe/<dedupe_type:re:[^/]*>')
@check_version
@USERS.auth()
def dedupe(dedupe_type):
    # TODO: nearidentical, identical
    # Given an image column, load it and compute the near-identical feature, for each image determine which ones are nearidentical
    start_row = bottle.request.params.get('startRow', '')
    stop_row = bottle.request.params.get('stopRow', '')
    col = bottle.request.params.get('column', '')
    table = bottle.request.params.get('table', '')
    if dedupe_type == 'identical':
        features = {}
        dedupe_feature = lambda x, y: features.setdefault(base64.b64encode(hashlib.md5(y).digest()), []).append(base64.b64encode(x))
    else:
        bottle.abort(400)
    
    for cur_row, cur_col in hadoopy_hbase.scanner_row_column(THRIFT, table, column=col,
                                                             start_row=start_row, per_call=10,
                                                             stop_row=stop_row):
        dedupe_feature(cur_row, cur_col)
    return {'data': features}


if __name__ == '__main__':
    import gevent.pywsgi
    SERVER = gevent.pywsgi.WSGIServer(('0.0.0.0', ARGS.port), bottle.app())
    SERVER.serve_forever()
