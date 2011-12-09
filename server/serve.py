from gevent import monkey
monkey.patch_all()
import bottle
import argparse
import time
bottle.debug(True)
bottle.BaseRequest.MEMFILE_MAX = 10 * 1024 ** 2  # NOTE(brandyn): This changes the default MEMFILE size, necessary for bottle.request.json to work
SERVER_VERSION = {'major': 0, 'minor': 0, 'patch': 0, 'branch': 'dv'}

# # # Decorators


def require_auth(func):
    """Authentication decorator

    This verifies that the user is able to access the requested resource, handles
    error code reporting if not, populates an auth_funcs dictionary of functions
    requiring authentication (anything requiring priveleges must be used from here).
    """
    def inner(*args, **kw):
        print('Auth Check[%s]' % (bottle.request.auth,))
        if bottle.request.auth != ('user', 'pass'):
            bottle.abort(401)
        else:
            return func(*args, **kw)
    return inner


def require_version(func):

    def inner(*args, **kw):
        if bottle.request.json['version'] != SERVER_VERSION:
            bottle.abort(403)
        else:
            return func(*args, **kw)
    return inner


def require_size(func):

    def inner(*args, **kw):
        if bottle.request.MEMFILE_MAX <= bottle.request.content_length:
            bottle.abort(413)
        else:
            return func(*args, **kw)
    return inner


def method_info(quality=0, doc='', author={}, url='', method='GET'):

    def inner0(func):

        def inner1(*args, **kw):
            quality_codes = dict((x, [x, y]) for x, y in enumerate(['unimplemented', 'preliminary implementation',
                                                                    'partial implementation', 'draft implementation',
                                                                    'alpha implementation', 'beta implementation',
                                                                    'production implementation']))
            out = func(*args, **kw)
            out['info'] = {'quality': quality_codes[quality], 'handler_name': func.__name__}
            if doc:
                out['info']['doc'] = doc
            if author:
                out['info']['author'] = author
            if url:
                out['info']['url'] = url
            return out
        return inner1
    return inner0


HANDLERS = {'/help/test': {'meth': }}

# # # Handlers: /help/

@bottle.get('/help/test.json')
@method_info(3, method='get')
def handler_help_test():
    bottle.response.content_type = 'application/json'
    return {'result': 'ok'}


@bottle.get('/help/configuration.json')
@method_info(1, ['get'])
def handler_help_configuration():
    bottle.response.content_type = 'application/json'
    return {'version': SERVER_VERSION,
            'max_request_size': bottle.BaseRequest.MEMFILE_MAX,
            'time': time.time()}


@bottle.get('/help/status.json')
@method_info()
def handler_help_status():
    bottle.response.content_type = 'application/json'
    return {}


# # # Handlers: /legal/

@bottle.get('/legal/privacy.json')
@method_info()
def handler_legal_privacy():
    bottle.response.content_type = 'application/json'
    return {'result': 'TODO'}


@bottle.get('/legal/tos.json')
@method_info()
def handler_legal_tos():
    bottle.response.content_type = 'application/json'
    return {'result': 'TODO'}


# # # Handlers: /analyze/

@bottle.put('/analyze/tags.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_analyze_tags():
    return {'result': {}}


@bottle.put('/analyze/objects.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_analyze_objects():
    return {'result': {}}


@bottle.put('/analyze/scene.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_analyze_scene():
    return {'result': {}}


@bottle.put('/analyze/location.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_analyze_location():
    return {'result': {}}


@bottle.put('/analyze/time.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_analyze_time():
    return {'result': {}}


@bottle.put('/analyze/who.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_analyze_who():
    return {'result': {}}


@bottle.put('/analyze/faces.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_analyze_faces():
    return {'result': {}}


@bottle.put('/analyze/rotate.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_analyze_rotate():
    return {'result': {}}


@bottle.put('/analyze/segments.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_analyze_segments():
    return {'result': {}}


# # # Handlers: /query/


@bottle.put('/query/similar.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_query_similar():
    return {'result': {}}


# # # Handlers: /process/


@bottle.put('/process/info.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_process_info():
    return {'result': {}}


@bottle.put('/process/register.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_process_register():
    return {'result': {}}


@bottle.put('/process/stabilize.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_process_stabilize():
    return {'result': {}}


@bottle.put('/process/convert.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_process_convert():
    return {'result': {}}


@bottle.put('/process/cluster.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_process_cluster():
    return {'result': {}}


@bottle.put('/process/points.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_process_points():
    return {'result': {}}


@bottle.put('/process/features.json')
@require_size
@require_auth
@require_version
@method_info()
def handler_process_features():
    return {'result': {}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take in visual data")
    parser.add_argument('--port', type=str, help='Run on this port (default 8080)',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
    
