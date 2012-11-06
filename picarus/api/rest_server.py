"""
/db/
/db/<table>/*/<col>?op=see/scene/indoor&input=//<in_col>
/db/<table>/*/<col>?op=scene/indoor&input=<out_table>/*/<out_col>
/db/<table>/<row>/<col>?vision=scene/indoor&input=<out_table>/<out_row>/<out_col>


/db/<table>/<col>?vision=scene/indoor

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
import distpy
from users import Users, UnknownUser
from picarus.modules import HashRetrievalClassifier
import picarus._features
import boto


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


def print_request():
    ks = ['auth', 'content_length', 'content_type', 'environ', 'fullpath', 'is_ajax', 'is_xhr', 'method', 'path', 'query_string', 'remote_addr', 'remote_route', 'script_name', 'url', 'urlparts']
    for k in ks:
        print('%s: %s' % (k, str(getattr(bottle.request, k))))

    print('%s: %s' % ('files', (getattr(bottle.request, 'files')).keys()))

    ks = ['forms', 'params', 'query', 'cookies', 'headers']
    for k in ks:
        print('%s: %s' % (k, str(dict(getattr(bottle.request, k)))))


@bottle.get('/stats')
@mimerender.map_exceptions(mapping=((ValueError, '500 Internal Server Error'),),
                           xml=render_xml_exception,
                           json=render_json_exception)
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
@USERS.auth(True)
def stats(auth_user):
    print(auth_user.user)
    return auth_user.stats()


# Working
# GET /db/t/r/c
# GET /db/t/r/
# PUT /db/t/r/c (data from params['data'] or files['data'])
# PUT /db/t/r/ (columns/data from params/files)
# DELETE /db/t/r/c
# DELETE /db/t/r/

# TODO
# PUT /db/t/r/c (function=function to perform (e.g., see/detect/faces), input=table/row/col)
# PUT /db/t/*/c (function=function to perform (e.g., see/detect/faces), input=table/*/col)

@bottle.put('/db/<table:re:[^/]*>/<row:re:[^/]*>/<col:re:[^/]*>')
@bottle.delete('/db/<table:re:[^/]*>/<row:re:[^/]*>/<col:re:[^/]*>')
@bottle.get('/db/<table:re:[^/]*>/<row:re:[^/]*>/<col:re:[^/]*>')
@mimerender.map_exceptions(mapping=((ValueError, '500 Internal Server Error'),),
                           xml=render_xml_exception,
                           json=render_json_exception)
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
@USERS.auth()
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
    if table != 'images':
        raise ValueError('Only images allowed for now!')
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
    elif method == 'PUT':
        mutations = []
        if col:
            if 'function' in bottle.request.params:
                # TODO: Handle row=*
                input_table, input_row, input_col = bottle.request.params['input'].split()
                result = THRIFT.get(table, row, col)
                if not result:
                    raise ValueError('Cell not found!')
                image = result[0].value
                # Remove internal parameters
                params = dict(bottle.request.params)
                del params['input']
                del params['function']
                output = _action_handle(bottle.request.params['function'], params, image)
                mutations.append(hadoopy_hbase.Mutation(column=col, value=output))
            else:
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
    print('ImageData[%s]' % str(data[:25]))
    return imfeat.image_fromstring(data), params

#@mimerender.map_exceptions(mapping=((ValueError, '500 Internal Server Error'),),
#                           xml=render_xml_exception,
#                           json=render_json_exception)
@bottle.post('/see/<request:re:.*>')
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
@USERS.auth()
def see(request):
    print_request()
    image, params = _get_image()
    return _action_handle('see/%s' % request, params, image)

FEATURE_FUN = [imfeat.GIST, imfeat.Histogram, imfeat.Moments, imfeat.TinyImage, imfeat.GradientHistogram]
FEATURE_FUN = dict((('see/feature/%s' % (c.__name__)), c) for c in FEATURE_FUN)
print('search')
SEARCH_FUN = {'see/search/logos': HashRetrievalClassifier().load(open('logo_index.pb').read()),
              'see/search/scenes': HashRetrievalClassifier().load(open('image_search/sun397_index.pb').read()),
              'see/search/masks': HashRetrievalClassifier().load(open('image_search/sun397_mask_index.pb').read())}
TP = pickle.load(open('tree_ser-texton.pkl'))  # TODO: support loading tp/tp2 as strings, move to imseg
TP2 = pickle.load(open('tree_ser-integral.pkl'))
TEXTON = picarus._features.TextonPredict(tp=TP, tp2=TP2, num_classes=9)
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


def _action_handle(function, params, image):
    print('Action[%s]' % function)
    try:
        ff = FEATURE_FUN[function]
        image = imfeat.resize_image_max_side(image, 320)  # TODO: Expose this
        return {'feature': ff(**params)(image).tolist()}
    except KeyError:
        pass
    try:
        sf = SEARCH_FUN[function]
        print(sf.feature)
        return {'results': sf.analyze_cropped(image)}
    except KeyError:
        pass
    if function == 'see/texton':
        image = cv2.resize(image, (320, int(image.shape[0] * 320. / image.shape[1])))
        image = np.ascontiguousarray(image)
        semantic_masks = TEXTON(image)
        texton_argmax2 = np.argmax(semantic_masks, 2)
        image_string = imfeat.image_tostring(COLORS_BGR[texton_argmax2], 'png')
        return {'argmax_pngb64': base64.b64encode(image_string)}
    if function == 'see/faces':
        results = [map(float, x) for x in FACES._detect_faces(image)]
        return {'faces': [{'tl_x': x[0], 'tl_y': x[1], 'width': x[2], 'height': x[3]}
                          for x in results]}
    return {}


@bottle.post('/image')
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
@USERS.auth()
def image():
    print_request()
    # TODO(Cleanup)
    image, params = _get_image()
    image = imfeat.resize_image_max_side(image, 320)
    image_string = imfeat.image_tostring(image, 'jpg')
    return {'jpgb64': base64.b64encode(image_string)}


#@bottle.get('/admin/stop')
#def stop():
#    # TODO: Do auth
#    SERVER.stop()


@bottle.get('/')
def index():
    return open('demo_all.html').read()


@bottle.get('/login')
def login():
    return open('login.html').read()


@bottle.get('/search')
def search():
    return open('image_search.html').read()


@bottle.post('/auth')
def auth():
    print_request()
    email = dict(bottle.request.params)['email']
    try:
        USERS.email_auth(email, bottle.request.remote_addr, bottle.request.params['recaptcha_challenge_field'], bottle.request.params['recaptcha_response_field'])
    except UnknownUser:
        bottle.abort(401)
    return 'Emailing auth code'

if __name__ == '__main__':
    import gevent.pywsgi
    SERVER = gevent.pywsgi.WSGIServer(('0.0.0.0', ARGS.port), bottle.app())
    SERVER.serve_forever()
