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
from picarus.modules.logos import LogoProcessor
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
            return {'data': THRIFT.get(table, row, col)}
        elif table and row:
            result = THRIFT.getRow(table, row)
            if not result:
                raise ValueError('Row not found!')
            return {'data': dict(result[0].columns)}
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
                mutations.append(hadoopy_hbase.Mutation(column=x, value=bottle.request.files[x].file.read()))
            for x in bottle.request.params:
                mutations.append(hadoopy_hbase.Mutation(column=x, value=bottle.request.files[x].file.read()))
            if not mutations:
                raise ValueError('No columns specified!')
        THRIFT.mutateRow(table, row, mutations)
        return {}
    elif method == 'DELETE':
        mutations = []
        if col:
            mutations.append(hadoopy_hbase.Mutation(column=col, isDelete=True))
        else:
            for x in bottle.request.files:
                mutations.append(hadoopy_hbase.Mutation(column=x, isDelete=True))
            for x in bottle.request.params:
                mutations.append(hadoopy_hbase.Mutation(column=x, isDelete=True))
            if not mutations:
                raise ValueError('No columns specified!')
        THRIFT.mutateRow(table, row, mutations)
        return {}
    else:
        raise ValueError

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
SEARCH_FUN = {'see/search/logos': LogoProcessor().load(open('logo_index.pb').read())}

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
    THRIFT = hadoopy_hbase.connect(ARGS.thrift_server, ARGS.thrift_port)
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
