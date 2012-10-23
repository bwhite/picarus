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
import hadoopy_hbase
import cPickle as pickle
import numpy as np
import cv2
from picarus.modules.logos import LogoProcessor
bottle.debug(True)


mimerender = mimerender.BottleMimeRender()
render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda **args: json.dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message
render_xml_exception = lambda exception: '<exception>%s</exception>' % exception.message
render_json_exception = lambda exception: json.dumps({'exception': exception.message})


def print_request():
    ks = ['auth', 'content_length', 'content_type', 'environ', 'fullpath', 'is_ajax', 'is_xhr', 'method', 'path', 'query_string', 'remote_addr', 'remote_route', 'script_name', 'url', 'urlparts']
    for k in ks:
        print('%s: %s' % (k, str(getattr(bottle.request, k))))

    print('%s: %s' % ('files', (getattr(bottle.request, 'files')).keys()))

    ks = ['forms', 'params', 'query', 'cookies', 'headers']
    for k in ks:
        print('%s: %s' % (k, str(dict(getattr(bottle.request, k)))))

@bottle.get('/echo/:value')
@bottle.put('/echo/:value')
@bottle.post('/echo/:value')
@mimerender.map_exceptions(mapping=((ValueError, '500 Internal Server Error'),),
                           xml=render_xml_exception,
                           json=render_json_exception)
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
def echo(value):
    print_request()
    return {'message': value}



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
def data(table, row, col):
    # TODO Check authentication
    method = bottle.request.method.upper()
    print_request()
    if table != 'testtable':
        raise ValueError('Only testtable allowed for now!')
    if method == 'GET':
        if table and row and col:
            result = THRIFT.get(table, row, col)
            if not result:
                raise ValueError('Cell not found!')
            return {'data': result[0].value}
        elif table and row:
            result = THRIFT.getRow(table, row)
            if not result:
                raise ValueError('Row not found!')
            return {'data': dict((x, y.value) for x, y in result[0].columns.items())}
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


#@mimerender.map_exceptions(mapping=((ValueError, '500 Internal Server Error'),),
#                           xml=render_xml_exception,
#                           json=render_json_exception)
@bottle.post('/see/<request:re:.*>')
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
def see(request):
    print_request()
    try:
        data = bottle.request.files['image'].file.read()
        print(data[:25])
        image = imfeat.image_fromstring(data)
    except KeyError:
        raise ValueError('Missing image')
    return _action_handle('see/%s' % request, dict(bottle.request.params), image)

FEATURE_FUN = [imfeat.GIST, imfeat.Histogram, imfeat.Moments, imfeat.TinyImage, imfeat.GradientHistogram]
FEATURE_FUN = dict((('see/feature/%s' % (c.__name__)), c) for c in FEATURE_FUN)
SEARCH_FUN = {'see/search/logos': LogoProcessor().load(open('logo_index.pb').read())}
TP = pickle.load(open('tree_ser-texton.pkl'))
TP2 = pickle.load(open('tree_ser-integral.pkl'))
TEXTON = imfeat.TextonBase(tp=TP, tp2=TP2, num_classes=9)
CLASS_COLORS = json.load(open('class_colors.js'))
COLORS_BGR = np.array([x[1]['color'][::-1] for x in sorted(CLASS_COLORS.items(), key=lambda x: x[1]['mask_num'])], dtype=np.uint8)
FACES = imfeat.Faces()

def _action_handle(function, params, image):
    print('Action[%s]' % function)
    try:
        ff = FEATURE_FUN[function]
        return {'feature': ff(**params)(image).tolist()}
    except KeyError:
        pass
    try:
        sf = SEARCH_FUN[function]
        return {'results': sf.analyze_cropped(image)}
    except KeyError:
        pass
    if function == 'see/texton':
        image = cv2.resize(image, (320, int(image.shape[0] * 320. / image.shape[1])))
        image = np.ascontiguousarray(image)
        semantic_masks = TEXTON._predict(image)[5]
        texton_argmax2 = np.argmax(semantic_masks, 2)
        image_string = imfeat.image_tostring(COLORS_BGR[texton_argmax2], 'png')
        return {'argmax_pngb64': base64.b64encode(image_string)}
    if function == 'see/faces':
        results = [map(float, x) for x in FACES._detect_faces(image)]
        return {'faces': [{'tl_x': x[0], 'tl_y': x[1], 'width': x[2], 'height': x[3]}
                          for x in results]}
    return {}


@bottle.get('/')
def index():
    return open('demo_all.html').read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Picarus REST Frontend')
    parser.add_argument('--port', default='8080')
    parser.add_argument('--thrift_server', default='localhost')
    parser.add_argument('--thrift_port', default='9090')
    ARGS = parser.parse_args()
    THRIFT = hadoopy_hbase.connect(ARGS.thrift_server, ARGS.thrift_port)
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
