
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
import redis
import hadoopy_hbase
import cPickle as pickle
import numpy as np
import cv2
import gevent
import crawlers
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
logging.basicConfig(level=logging.DEBUG)

VERSION = 'a0'


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


def print_request():
    ks = ['auth', 'content_length', 'content_type', 'environ', 'fullpath', 'is_ajax', 'is_xhr', 'method', 'path', 'query_string', 'remote_addr', 'remote_route', 'script_name', 'url', 'urlparts']
    for k in ks:
        print('%s: %s' % (k, str(getattr(bottle.request, k))))

    print('%s: %s' % ('files', (getattr(bottle.request, 'files')).keys()))

    ks = ['forms', 'params', 'query', 'cookies', 'headers']
    for k in ks:
        print('%s: %s' % (k, str(dict(getattr(bottle.request, k)))))


@bottle.get('/<version:re:[^/]*>/user/stats')
@mimerender.map_exceptions(mapping=((ValueError, '500 Internal Server Error'),),
                           xml=render_xml_exception,
                           json=render_json_exception)
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
@USERS.auth(True)
@check_version
def stats(auth_user):
    print(auth_user.user)
    return auth_user.stats()


@bottle.put('/<version:re:[^/]*>/data/<table:re:[^/]*>/<row:re:[^/]*>/<col:re:[^/]*>')
@bottle.delete('/<version:re:[^/]*>/data/<table:re:[^/]*>/<row:re:[^/]*>/<col:re:[^/]*>')
@bottle.get('/<version:re:[^/]*>/data/<table:re:[^/]*>/<row:re:[^/]*>/<col:re:[^/]*>')
@mimerender.map_exceptions(mapping=((ValueError, '500 Internal Server Error'),),
                           xml=render_xml_exception,
                           json=render_json_exception)
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
@USERS.auth()
@check_version
def data(table, row, col):
    try:
        THRIFT_LOCK.acquire()
        return _data(table, row, col)
    finally:
        THRIFT_LOCK.release()


def _data(table, row, col):
    row = base64.urlsafe_b64decode(row)
    col = base64.urlsafe_b64decode(col)
    method = bottle.request.method.upper()
    print_request()
    # TODO Check authentication per table
    if table not in ('images', 'testtable'):
        raise ValueError('Only images/testtable allowed for now!')
    if method == 'GET':
        if table and row and col:
            result = THRIFT.get(table, row, col)
            if not result:
                raise ValueError('Cell not found!')
            return {'data': base64.b64encode(result[0].value)}
        elif table and row:
            result = THRIFT.getRow(table, row)
            if not result:
                raise ValueError('Row not found!')
            return {'data': dict((x, base64.b64encode(y.value)) for x, y in result[0].columns.items())}
        elif table:
            # TODO: Need to verify limits on this scan and check auth
            num_rows = min(101, int(bottle.request.params.get('maxRows', 1)))
            out = {}
            start_row = base64.urlsafe_b64decode(bottle.request.params.get('startRow', ''))
            stop_row = base64.urlsafe_b64decode(bottle.request.params.get('stopRow', ''))
            stop_row = stop_row if stop_row else None
            if col:
                print 'columns', [col]
                for cur_row, cur_col in hadoopy_hbase.scanner_row_column(THRIFT, table, column=col,
                                                                         start_row=start_row, per_call=num_rows,
                                                                         stop_row=stop_row, max_rows=num_rows):
                    out[base64.b64encode(cur_row)] = base64.b64encode(cur_col)
            else:
                columns = map(base64.urlsafe_b64decode, bottle.request.params.getall('column'))
                print 'columns', columns
                for cur_row, cur_columns in hadoopy_hbase.scanner(THRIFT, table, columns=columns,
                                                                  start_row=start_row, per_call=num_rows,
                                                                  stop_row=stop_row, max_rows=num_rows):
                    out[base64.b64encode(cur_row)] = {base64.b64encode(k): base64.b64encode(v) for k, v in cur_columns.items()}
            return {'data': out}
    elif method == 'PUT':
        mutations = []
        if col:
            if 'data' in bottle.request.files:
                mutations.append(hadoopy_hbase.Mutation(column=col, value=bottle.request.files['data'].file.read()))
            elif 'data' in bottle.request.params:
                mutations.append(hadoopy_hbase.Mutation(column=col, value=bottle.request.params['data']))
            else:
                raise ValueError('"data" must be specified!')
        else:
            for x in bottle.request.files:
                THRIFT.mutateRow(table, row, [hadoopy_hbase.Mutation(column=x, value=bottle.request.files[x].file.read())])
            for x in set(bottle.request.params) - set(bottle.request.files):
                mutations.append(hadoopy_hbase.Mutation(column=x, value=bottle.request.params[x]))
            if not mutations and len(bottle.request.files) == 0:
                raise ValueError('No columns specified!')
        if mutations:
            THRIFT.mutateRow(table, row, mutations)
        return {}
    elif method == 'DELETE':
        mutations = []
        if col:
            mutations.append(hadoopy_hbase.Mutation(column=col, isDelete=True))
        else:
            THRIFT.deleteAllRow(table, row)
        return {}
    else:
        raise ValueError


def _get_image():
    params = dict(bottle.request.params)
    try:
        data = base64.b64decode(params['image_b64'])
        del params['image_b64']
    except KeyError:
        try:
            data = bottle.request.files['image'].file.read()
        except KeyError:
            raise ValueError('Missing image')
    return data, imfeat.image_fromstring(data), params


@bottle.post('/<version:re:[^/]*>/see/<request:re:.*>')
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
@USERS.auth()
@check_version
def see(request):
    print_request()
    data, image, params = _get_image()
    return _action_handle('see/%s' % request, params, image, data)

FEATURE_FUN = [imfeat.GIST, imfeat.Histogram, imfeat.Moments, imfeat.TinyImage, imfeat.GradientHistogram]
FEATURE_FUN = dict((('see/feature/%s' % (c.__name__)), c) for c in FEATURE_FUN)
print('search')
# TODO Fix
CLASSIFY_FUN = {}


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


CLASSIFY_FUN = {'see/classify/indoor': picarus.api.image_classifier_frompb(MANAGER.key_to_classifier_pb('pred:h\x90\xf57\\\x8az\x0f\xd0K\xb6\xbc\xd7\taG\xa61l\x9b'))}
LOGO_KEY = 'pred:3aA\x980L\xdf\xbb\xf4\xc7K\xca7\xc7\xd2\x84\x8d\xf4\x98"'  # good logo
LOGO_KEY = 'pred:\x1b_q\x7f\xc6\x05:\x18hS\xd6\xdb\xf2\x88\xa0Z\xec\xd5\x14\xee'  # google
LANDMARKS_KEY = "pred:e\x03\xd1\x9f\xd1\xd4m\xb6'k\x17#\x06\x0c\xacW\xfa\x93z\x1d"  # flickr surf
#LANDMARKS_KEY = 'pred:\x89\xd31\x1e\x85\x8f\xac\xbf\xab\x9eNQ4\x81\xca\xb5\xb0\xf9\xb4h'  # flickr color
CLASSIFY_FUN['see/classify/logos'] = picarus.api.image_classifier_frompb(MANAGER.key_to_classifier_pb(LOGO_KEY))
CLASSIFY_FUN['see/classify/landmarks'] = picarus.api.image_classifier_frompb(MANAGER.key_to_classifier_pb(LANDMARKS_KEY))

SEARCH_FUN = {}
#SEARCH_FUN = {'see/search/logos': HashRetrievalClassifier().load(open('logo_index.pb').read()),
#              'see/search/scenes': HashRetrievalClassifier().load(open('image_search/feature_index.pb').read()),
#              'see/search/masks': HashRetrievalClassifier().load(open('image_search/sun397_masks_index.pb').read())}


def _get_texton():
    forests = []
    threshs = [0.]
    for x in ['outdoor', 'indoor']:
        tp = pickle.load(open('tree_ser-%s-texton.pkl' % x))
        tp2 = pickle.load(open('tree_ser-%s-integral.pkl' % x))
        forests.append({'tp': tp, 'tp2': tp2})
    return picarus._features.TextonILPPredict(num_classes=8, ilp=MANAGER.key_to_classifier_pb('pred:h\x90\xf57\\\x8az\x0f\xd0K\xb6\xbc\xd7\taG\xa61l\x9b').SerializeToString(),
                                              forests=forests, threshs=threshs)


TEXTON = _get_texton()
#ILP_WEIGHTS = json.load(open('ilp_weights.js'))
#ILP_WEIGHTS['ilp_tables'] = np.array(ILP_WEIGHTS['ilp_tables'])

#TEXTON = pickle.loads(pickle.dumps(TEXTON, -1))
#SEARCH_FUN['see/search/masks'].feature = lambda x: [TEXTON._predict(imfeat.resize_image_max_side(x, 320))[5]]

#print('hasher')
#hasher = SEARCH_FUN['see/search/masks'].hasher
#class_params = sorted(hasher.class_params.items(), key=lambda x: [0])
#weights = np.hstack([x[1]['w'] for x in class_params])
#SEARCH_FUN['see/search/masks'].index._d = distpy.JaccardWeighted(weights)  # TODO: Support Cython deserialization
#print(weights)

CLASS_COLORS = json.load(open('class_colors.js'))
COLORS_BGR = np.array([x[1]['color'][::-1] for x in sorted(CLASS_COLORS.items(), key=lambda x: x[1]['mask_num'])], dtype=np.uint8)
FACES = imfeat.Faces()
COLOR_NAMING = imfeat.ColorNaming()


def _action_handle(function, params, image, data):
    print('Action[%s]' % function)
    try:
        ff = FEATURE_FUN[function]
        image = imfeat.resize_image_max_side(image, 320)  # TODO: Expose this
        return {'feature': ff(**params)(image).tolist()}
    except KeyError:
        pass
    try:
        sf = SEARCH_FUN[function]
        image = imfeat.resize_image_max_side(image, 320)  # TODO: Expose this
        print(sf.feature)
        out = {'results': sf.analyze_cropped(image)}
        if function == 'see/search/masks':
            out['classes'] = CLASS_COLORS
        return out
    except KeyError:
        pass
    try:
        cf = CLASSIFY_FUN[function]
        return {'results': cf(data)}
    except KeyError:
        pass
    if function == 'see/texton':  # or function == 'see/texton_ilp'
        image = cv2.resize(image, (320, int(image.shape[0] * 320. / image.shape[1])))
        image = np.ascontiguousarray(image)
        semantic_masks = TEXTON(image)
        if function == 'see/texton_ilp':
            ilp_pred = CLASSIFY_FUN['see/classify/indoor'](imfeat.resize_image_max_side(image, 320))
            try:
                bin_index = [x for x, y in enumerate(ILP_WEIGHTS['bins']) if y >= ilp_pred][0]
            except IndexError:
                bin_index = ILP_WEIGHTS['ilp_tables'].shape[1]
            if bin_index != 0:
                bin_index -= 1
            ilp_weights = ILP_WEIGHTS['ilp_tables'][:, bin_index]
            print('ILP Pred[%s] Weights[%s]' % (ilp_pred, ilp_weights))
            semantic_masks *= ilp_weights
        #min_probability = float(params.get('min_probability', 0.5))
        #semantic_masks = np.dstack([semantic_masks, np.ones_like(semantic_masks[:, :, 0]) * min_probability])
        texton_argmax2 = np.argmax(semantic_masks, 2)
        image_string = imfeat.image_tostring(COLORS_BGR[texton_argmax2], 'png')
        out = {'argmax_pngb64': base64.b64encode(image_string)}
        out['classes'] = CLASS_COLORS
        return out
    if function == 'see/colors':
        image = cv2.resize(image, (320, int(image.shape[0] * 320. / image.shape[1])))
        image = np.ascontiguousarray(image)
        masks = COLOR_NAMING.make_feature_mask(image)
        mask_argmax = np.argmax(masks, 2)
        image_string = imfeat.image_tostring(COLOR_NAMING.color_values[mask_argmax], 'png')
        return {'argmax_pngb64': base64.b64encode(image_string)}
    if function == 'see/faces':
        results = [map(float, x) for x in FACES._detect_faces(image)]
        return {'faces': [{'tl_x': x[0], 'tl_y': x[1], 'width': x[2], 'height': x[3]}
                          for x in results]}
    return {}


@bottle.post('/<version:re:[^/]*>/image')
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
@USERS.auth()
@check_version
def image():
    print_request()
    # TODO(Cleanup)
    data, image, params = _get_image()
    image = imfeat.resize_image_max_side(image, 320)
    image_string = imfeat.image_tostring(image, 'jpg')
    return {'jpgb64': base64.b64encode(image_string)}


@bottle.get('/<version:re:[^/]*>/models')
@USERS.auth()
@check_version
def models():
    out = {}  # [type][row_id]
    prefix_to_name = {'feat:': 'feature',
                      'mfeat:': 'multi-feature',
                      'mask:': 'mask-feature',
                      'pred:': 'classifier',
                      'srch:': 'index',
                      'hash:': 'hasher',
                      'data:': 'preprocessor'}
    try:
        THRIFT_LOCK.acquire()
        for row, cols in hadoopy_hbase.scanner(THRIFT, 'picarus_models', columns=['data:input', 'data:versions', 'data:prefix', 'data:creation_time']):
            name = prefix_to_name[cols['data:prefix']]
            out.setdefault(name, {})[base64.b64encode(row)] = {'inputs': json.loads(cols['data:input']),
                                                               'versions': json.loads(cols['data:versions']),
                                                               'creationTime': float(cols['data:creation_time'])}
    finally:
        THRIFT_LOCK.release()
    return out


#@bottle.get('/admin/stop')
#def stop():
#    # TODO: Do auth
#    SERVER.stop()

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

if __name__ == '__main__':
    import gevent.pywsgi
    SERVER = gevent.pywsgi.WSGIServer(('0.0.0.0', ARGS.port), bottle.app())
    SERVER.serve_forever()
