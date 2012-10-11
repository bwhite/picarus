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

bottle.debug(True)


mimerender = mimerender.BottleMimeRender()
render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda **args: json.dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message
render_xml_exception = lambda exception: '<exception>%s</exception>' % exception.message
render_json_exception = lambda exception: json.dumps({'exception': exception.message})

DB = {'test_table': {}}  # [table][row][col] = val



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


@bottle.put('/db/:table/:row/:col')
@bottle.delete('/db/:table/:row/:col')
@bottle.get('/db/:table/:row/:col')
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
    if method == 'GET':
        return {'value': DB[table][row][col]}
    elif method == 'PUT':
        DB[table].setdefault(row, {})[col] = bottle.request.files['data'].file.read()
        return {}
    elif method == 'DELETE':
        return {}
    else:
        raise ValueError
    return {'message': [table, row, col]}

#@mimerender.map_exceptions(mapping=((ValueError, '500 Internal Server Error'),),
#                           xml=render_xml_exception,
#                           json=render_json_exception)
@bottle.post('/see/feature/:feature')
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
def see_feature(feature):
    print_request()
    return _action_handle('see/feature/' + feature, dict(bottle.request.params), dict(bottle.request.files))

#@mimerender.map_exceptions(mapping=((ValueError, '500 Internal Server Error'),),
#                           xml=render_xml_exception,
#                           json=render_json_exception)
@bottle.post('/see/search/logos')
@mimerender(default='json',
            html=render_html,
            xml=render_xml,
            json=render_json,
            txt=render_txt)
def see_search():
    print_request()
    return _action_handle('see/search/logos', dict(bottle.request.params), dict(bottle.request.files))



FEATURE_FUN = [imfeat.GIST, imfeat.Histogram, imfeat.Moments, imfeat.TinyImage, imfeat.GradientHistogram]
FEATURE_FUN = dict((('see/feature/%s' % (c.__name__)), c) for c in FEATURE_FUN)
SEARCH_FUN = {'see/search/logos': LogoProcessor().load(open('index.pb').read())}

def _action_handle(function, params, files):
    try:
        image = imfeat.image_fromstring(files['image'].file.read())
    except KeyError:
        raise ValueError('Missing image')
    try:
        ff = FEATURE_FUN[function]
        return {'feature': ff(**params)(image).tolist()}
    except KeyError:
        pass
    try:
        sf = SEARCH_FUN[function]
        return {'results': [json.loads(x)[0] for x in sf.analyze_cropped(image)]}
    except KeyError:
        pass
    
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
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
