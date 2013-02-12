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
from flickr_keys import FLICKR_API_KEY, FLICKR_API_SECRET
logging.basicConfig(level=logging.DEBUG)

VERSION = 'a1'


def check_version(func):

    def inner(version, *args, **kw):
        if version != VERSION:
            bottle.abort(400)
        return func(*args, **kw)
    return inner


def verify_slice_permissions(prefixes, permissions, start_row, stop_row):
    permissions = set(permissions)
    prefixes = [x for x, y in prefixes.items() if set(y).issuperset(permissions)]
    for prefix in prefixes:
        if prefix == '':
            return
        # NOTE: Prevents rollover, minor limitation on prefix is that it must not end in \xff
        assert prefix[-1] != '\xff'
        prefix_start_row = prefix
        prefix_stop_row = prefix[:-1] + chr(ord(prefix[-1]) + 1)
        if start_row and prefix_start_row <= start_row < prefix_stop_row and stop_row and prefix_start_row <= stop_row <= prefix_stop_row:
            return
    bottle.abort(401)


def verify_row_permissions(prefixes, permissions, row):
    permissions = set(permissions)
    prefixes = [x for x, y in prefixes.items() if set(y).issuperset(permissions)]
    for prefix in prefixes:
        if prefix == '':
            return
        # NOTE: Prevents rollover, minor limitation on prefix is that it must not end in \xff
        assert prefix[-1] != '\xff'
        prefix_start_row = prefix
        prefix_stop_row = prefix[:-1] + chr(ord(prefix[-1]) + 1)
        if row and prefix_start_row <= row < prefix_stop_row:
            return
    bottle.abort(401)


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
        verify_row_permissions(auth_user.image_prefixes, 'w', row)
        mutations = []
        # TODO: Reuse PATCH code which also does this
        for x in bottle.request.files:
            thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=bottle.request.files[x].file.read())])
        for x in set(bottle.request.params) - set(bottle.request.files):
            print('ParmLen[%d]' % len(bottle.request.params[x]))
            print('md5[%s]' % hashlib.md5(bottle.request.params[x]).hexdigest())
            mutations.append(hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=bottle.request.params[x]))
        if mutations:
            thrift.mutateRow(table, row, mutations)
        return {'row': base64.urlsafe_b64encode(row)}


def _user_to_dict(user):
    return {'stats': user.stats(), 'uploadRowPrefix': user.upload_row_prefix, 'email': user.user, 'imagePrefixes': user.image_prefixes}


@bottle.get('/<version:re:[^/]*>/users')
@USERS.auth(True)  # TODO: Make admin decorator
@check_version
def users(auth_user):
    if auth_user.user != 'bwhite@dappervision.com':  # Only me for now
        bottle.abort(401)
    bottle.response.headers["Content-type"] = "application/json"
    return json.dumps([_user_to_dict(USERS.get_user(u)) for u in USERS.list_users()])


@bottle.get('/<version:re:[^/]*>/users/<user:re:[^/]+>')
@USERS.auth(True)
@check_version
def data_row(auth_user, user):
    if auth_user.user != user:
        bottle.abort(401)
    bottle.response.headers["Content-type"] = "application/json"
    return _user_to_dict(auth_user)

@bottle.route('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>', 'PATCH')
@bottle.post('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@bottle.delete('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@bottle.get('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@USERS.auth(True)
@check_version
def data_row(auth_user, table, row):
    with thrift_lock() as thrift:
        row = base64.urlsafe_b64decode(row)
        method = bottle.request.method.upper()
        # TODO Check authentication per table
        if not (table and row):
            bottle.abort(400)
        if table not in ('images'):
            bottle.abort(400)
        if method == 'GET':
            verify_row_permissions(auth_user.image_prefixes, 'r', row)
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
            verify_row_permissions(auth_user.image_prefixes, 'w', row)
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
            image_column = base64.urlsafe_b64decode(bottle.request.params['imageColumn'])
            results = thrift.get(table, row, image_column)
            if not results:
                print((table, row, image_column))
                bottle.abort(404)
            if action == 'i/classify':
                verify_row_permissions(auth_user.image_prefixes, 'r', row)
                classifier = _classifier_from_key(base64.urlsafe_b64decode(bottle.request.params['model']))
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps(classifier(results[0].value))
            elif action == 'i/search':
                verify_row_permissions(auth_user.image_prefixes, 'r', row)
                index = _index_from_key(base64.urlsafe_b64decode(bottle.request.params['model']))
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps(index(results[0].value))
            elif action == 'io/thumbnail':
                # TODO
                verify_row_permissions(auth_user.image_prefixes, 'rw', row)
                raise ValueError('not implemented')
                return json.dumps({})
            else:
                bottle.abort(400)
        elif method == 'DELETE':
            verify_row_permissions(auth_user.image_prefixes, 'w', row)
            thrift.deleteAllRow(table, row)
            return {}
        else:
            bottle.abort(400)


@bottle.delete('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>/<col:re:[^/]+>')
@USERS.auth(True)
@check_version
def data_row_col(auth_user, table, row, col):
    with thrift_lock() as thrift:
        row = base64.urlsafe_b64decode(row)
        verify_row_permissions(auth_user.image_prefixes, 'w', row)
        col = base64.urlsafe_b64decode(col)
        if table not in ('images'):
            bottle.abort(400)
        thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=col, isDelete=True)])
        return {}


SCANNER_CACHE = {}  # [(start_row, end_row, col, max_rows, cursor, user)]


@bottle.post('/<version:re:[^/]*>/slice/<table:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>')
@bottle.get('/<version:re:[^/]*>/slice/<table:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>')
@USERS.auth(True)
@check_version
def data_rows(auth_user, table, start_row, stop_row):
    print_request()
    # TODO: Namespace cursors for each user
    with thrift_lock() as thrift:
        start_row = base64.urlsafe_b64decode(start_row)
        stop_row = base64.urlsafe_b64decode(stop_row)
        method = bottle.request.method.upper()
        columns = map(base64.urlsafe_b64decode, sorted(bottle.request.params.getall('column')))
        # TODO Check authentication per table
        if table not in ('images',):
            raise ValueError('Only images allowed for now!')
        if method == 'GET':
            verify_slice_permissions(auth_user.image_prefixes, 'r', start_row, stop_row)
            # TODO: Need to verify limits on this scan and check auth
            max_rows = min(100, int(bottle.request.params.get('maxRows', 1)))
            filter_string = bottle.request.params.get('filter')
            print('filter string[%s]' % filter_string)
            exclude_start = bool(int(bottle.request.params.get('excludeStart', 0)))
            cursor = bottle.request.params.get('cacheKey', '')
            # TODO: Allow user to specify cursor, then we can output just the rows
            try:
                if not exclude_start or not cursor:
                    raise KeyError
                scanner_key = (start_row, stop_row, tuple(columns), max_rows, cursor, filter_string, auth_user.user)
                scanner = SCANNER_CACHE[scanner_key]
                print('Reusing cached scanner [%s]' % str(scanner_key))
                del SCANNER_CACHE[scanner_key]
                exclude_start = False
            except KeyError:
                scanner = hadoopy_hbase.scanner(thrift, table, columns=columns,
                                                start_row=start_row, per_call=max_rows,
                                                stop_row=stop_row, filter=filter_string)
            stopped_early = False
            out = []
            for row_num, (cur_row, cur_columns) in enumerate(scanner, 1):
                if exclude_start and row_num == 1:
                    continue
                cur_out = {base64.urlsafe_b64encode(k): base64.b64encode(v) for k, v in cur_columns.items()}
                cur_out['row'] = base64.urlsafe_b64encode(cur_row)
                out.append(cur_out)
                if len(out) >= max_rows:
                    stopped_early = True
                    break
            if stopped_early and cursor:
                SCANNER_CACHE[(cur_row, stop_row, tuple(columns), max_rows, cursor)] = scanner
            bottle.response.headers["Content-type"] = "application/json"
            return json.dumps(out)
        elif method == 'POST':
            action = bottle.request.params['action']
            if action == 'io/thumbnail':
                verify_slice_permissions(auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running thumb')
                MANAGER.image_thumbnail(start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/preprocess':
                verify_slice_permissions(auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running preprocessor')
                MANAGER.image_preprocessor(base64.urlsafe_b64decode(bottle.request.params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/classify':
                verify_slice_permissions(auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running classifier')
                MANAGER.feature_to_prediction(base64.urlsafe_b64decode(bottle.request.params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/feature':
                verify_slice_permissions(auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running feature')
                MANAGER.image_to_feature(base64.urlsafe_b64decode(bottle.request.params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'i/dedupe/identical':
                col = base64.urlsafe_b64decode(bottle.request.params['column'])
                features = {}
                dedupe_feature = lambda x, y: features.setdefault(base64.b64encode(hashlib.md5(y).digest()), []).append(base64.urlsafe_b64encode(x))
                print('Running dedupe')
                for cur_row, cur_col in hadoopy_hbase.scanner_row_column(THRIFT, table, column=col,
                                                                         start_row=start_row, per_call=10,
                                                                         stop_row=stop_row):
                    dedupe_feature(cur_row, cur_col)
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps([{'rows': y} for x, y in features.items() if len(y) > 1])
            elif action == 'o/crawl/flickr':
                verify_slice_permissions(auth_user.image_prefixes, 'w', start_row, stop_row)
                # Only slices where the start_row can be used as a prefix may be used
                assert start_row and ord(start_row[-1]) != 255 and start_row[:-1] + chr(ord(start_row[-1]) + 1) == stop_row
                print('Running flickr')
                p = {}
                row_prefix = start_row
                assert row_prefix.find(':') != -1
                class_name = bottle.request.params['className']
                query = bottle.request.params.get('query')
                query = class_name if query is None else query
                p['api_key'] = bottle.request.params.get('apiKey', FLICKR_API_KEY)
                p['api_secret'] = bottle.request.params.get('apiSecret', FLICKR_API_SECRET)
                if 'hasGeo' in bottle.request.params:
                    p['has_geo'] = True
                try:
                    p['min_upload_date'] = int(bottle.request.params['minUploadDate'])
                except KeyError:
                    pass
                try:
                    p['max_upload_date'] = int(bottle.request.params['maxUploadDate'])
                except KeyError:
                    pass
                try:
                    p['page'] = int(bottle.request.params['page'])
                except KeyError:
                    pass
                return {'data': {'numRows': crawlers.flickr_crawl(crawlers.HBaseCrawlerStore(row_prefix), class_name, query, **p)}}
            elif action in ('io/annotate/image/query', 'io/annotate/image/entity'):
                global MTURK_SERVER
                if MTURK_SERVER is not None:
                    bottle.abort(500)  # Need to garbage collect these
                secret = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]
                p = {}
                image_column = base64.urlsafe_b64decode(bottle.request.params['imageColumn'])
                if action == 'io/annotate/image/entity':
                    entity_column = base64.urlsafe_b64decode(bottle.request.params['entityColumn'])
                    p['data'] = 'hbase://localhost:9090/images/%s/%s?entity=%s&image=%s' % (start_row, stop_row, entity_column, image_column)
                    p['type'] = 'image_entity'
                elif action == 'io/annotate/image/query':
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
            elif action.startswith('i/train/'):
                path = action[8:]

                def classifier_sklearn(model_dict, model_param, inputs):
                    print(inputs)
                    print(model_param)
                    row_cols = hadoopy_hbase.scanner(THRIFT, table,
                                                     columns=[inputs['feature'], inputs['meta']], start_row=start_row, stop_row=stop_row)
                    label_features = {0: [], 1: []}
                    for row, cols in row_cols:
                        print(repr(row))
                        label = int(cols[inputs['meta']] == model_param['class_positive'])
                        label_features[label].append(cols[inputs['feature']])
                    labels = [0] * len(label_features[0]) + [1] * len(label_features[1])
                    features = label_features[0] + label_features[1]
                    features = np.asfarray([picarus.api.np_fromstring(x) for x in features])
                    classifier = call_import(model_dict)
                    classifier.fit(features, np.asarray(labels))
                    return classifier
                print(path)
                if path == 'classifier/svmlinear':
                    return _create_model_from_params(path, classifier_sklearn)
                else:
                    bottle.abort(400)
            else:
                bottle.abort(400)
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


def _index_from_key(key):
    loader = lambda x: call_import(x) if isinstance(x, dict) else x
    input, index, param = MANAGER.key_to_input_model_param(key)
    input, hasher, param = MANAGER.key_to_input_model_param(input['hash'])
    hasher = loader(hasher)
    input, feature, param = MANAGER.key_to_input_model_param(input['feature'])
    feature = loader(feature)
    input, preprocessor, param = MANAGER.key_to_input_model_param(input['image'])
    preprocessor = loader(preprocessor)
    return lambda x: [json.loads(index.metadata[y]) for y in index.search_hash_knn(hasher(feature(preprocessor.asarray(x))).ravel(), 10)]


def _get_texton():
    forests = []
    threshs = [0.]
    for x in ['outdoor', 'indoor']:
        tp = pickle.load(open('tree_ser-%s-texton.pkl' % x))
        tp2 = pickle.load(open('tree_ser-%s-integral.pkl' % x))
        forests.append({'tp': tp, 'tp2': tp2})
    return picarus._features.TextonILPPredict(num_classes=8, ilp=MANAGER.key_to_classifier_pb('pred:h\x90\xf57\\\x8az\x0f\xd0K\xb6\xbc\xd7\taG\xa61l\x9b').SerializeToString(),
                                              forests=forests, threshs=threshs)


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


# [name]: {module, params}  where params is dict with "name" as key with value {'required': bool, type: (int or float), min, max} with [min, max) or {'required': bool, type: 'bool'} or {'required': enum, vals: [val0, val1, ...]}
PARAM_SCHEMAS = []
PARAM_SCHEMAS.append({'name': 'preprocessor',
                      'type': 'preprocessor',
                      'module': 'imfeat.ImagePreprocessor',
                      'data': 'none',   # none, row, slice
                      'inputs': ['raw_image'],  # abstract columns to be used for input
                      'modelParams': {},
                      'moduleParams': {'compression': {'type': 'enum', 'values': ['jpg']},
                                       'size': {'type': 'int', 'min': 32, 'max': 1025},
                                       'method': {'type': 'enum', 'values': ['force_max_side', 'max_side', 'force_square']}}})

PARAM_SCHEMAS.append({'name': 'histogram',
                      'type': 'feature',
                      'data': 'none',
                      'inputs': ['processed_image'],
                      'module': 'imfeat.Histogram',
                      'modelParams': {'feature_type': {'type': 'const', 'value': 'feature'}},
                      'moduleParams': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                           'hsv', 'luv', 'hls', 'lab', 'gray']},
                                       'num_bins': {'type': 'int', 'min': 1, 'max': 17},
                                       'style': {'type': 'enum', 'values': ['joint', 'planar']}}})

PARAM_SCHEMAS.append({'name': 'svmlinear',
                      'type': 'classifier',
                      'data': 'slice',
                      'inputs': ['feature', 'meta'],
                      'module': 'sklearn.svm.LinearSVC',
                      'modelParams': {'class_positive': {'type': 'str'}, 'classifier_type': {'type': 'const', 'value': 'sklearn_decision_func'}},
                      'moduleParams': {}})

for x in PARAM_SCHEMAS:
    x['path'] = '/'.join([x['type'], x['name']])

PARAM_SCHEMAS_SERVE = {}
for schema in PARAM_SCHEMAS:
    PARAM_SCHEMAS_SERVE[schema['path']] = dict(schema)


# TODO: Replace this, it is temporary
@bottle.get('/<version:re:[^/]*>/params')
@USERS.auth()
@check_version
def features():
    bottle.response.headers["Content-type"] = "application/json"
    return json.dumps(PARAM_SCHEMAS)


def _parse_params(schema, prefix):
    kw = {}
    params = schema[prefix + 'Params']
    get_param = lambda x: bottle.request.params[prefix + '-' + x]
    print(params)
    for param_name, param in params.items():
        print((param_name, param))
        if param['type'] == 'enum':
            param_value = get_param(param_name)
            if param_value not in param['values']:
                print(3)
                bottle.abort(400)
            kw[param_name] = param_value
        elif param['type'] == 'int':
            param_value = int(get_param(param_name))
            if not (param['min'] <= param_value < param['max']):
                print(2)
                bottle.abort(400)
            kw[param_name] = param_value
        elif param['type'] == 'const':
            kw[param_name] = param['value']
        elif param['type'] == 'str':
            kw[param_name] = get_param(param_name)
        else:
            print(1)
            bottle.abort(400)
    return kw


def _create_model_from_params(path, create_model):
    try:
        schema = PARAM_SCHEMAS_SERVE[path]
        model_params = _parse_params(schema, 'model')
        module_params = _parse_params(schema, 'module')
        print(model_params)
        print(module_params)
        model_dict = {'name': schema['module'], 'kw': module_params}
        get_key = lambda x: base64.urlsafe_b64decode(bottle.request.params['key-' + x])   # TODO: Verify that model keys exist
        prefix = {'feature': 'feat:', 'preprocessor': 'data:', 'classifier': 'pred:'}[schema['type']]
        inputs = {x: get_key(x) for x in schema['inputs']}
        model = create_model(model_dict, model_params, inputs)
        row = MANAGER.input_model_param_to_key(prefix, input=inputs, model=model, name=MANAGER.model_to_name(model_dict), param=model_params)
        return {'row': base64.urlsafe_b64encode(row)}
    except ValueError:
        print(0)
        bottle.abort(400)


@bottle.post('/<version:re:[^/]*>/models/<path:re:.*>')
@USERS.auth()
@check_version
def models_create(path):
    print_request()
    try:
        #model = call_import(model_dict)
        return _create_model_from_params(path, lambda model_dict, model_params, inputs: model_dict)
    except KeyError:
        bottle.abort(400)


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
    bottle.response.headers["Content-type"] = "application/json"
    return json.dumps(out)


@bottle.get('/static/<name:re:[^/]+>')
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


MTURK_SERVER = None


def _mturk_wrapper(*args, **kw):
    bottle.app[0] = bottle.Bottle()  # Clear previous app
    import mturk_vision
    out = mturk_vision.server(*args, **kw)
    print('Filtering based on annotations')
    MANAGER.filter_annotations_to_hbase()
    return out

if __name__ == '__main__':
    import gevent.pywsgi
    SERVER = gevent.pywsgi.WSGIServer(('0.0.0.0', ARGS.port), bottle.app())
    SERVER.serve_forever()
