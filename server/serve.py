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


# # # Handlers: /help/


@bottle.get('/help/test.json')
def handler_help_test():
    bottle.response.content_type = 'application/json'
    return '"ok"'


@bottle.get('/help/configuration.json')
def handler_help_configuration():
    bottle.response.content_type = 'application/json'
    return {'version': SERVER_VERSION,
            'max_request_size': bottle.BaseRequest.MEMFILE_MAX,
            'time': time.time()}


@bottle.get('/help/status.json')
def handler_help_status():
    bottle.response.content_type = 'application/json'
    return {}


# # # Handlers: /legal/


@bottle.get('/legal/privacy.json')
def handler_legal_privacy():
    bottle.response.content_type = 'application/json'
    return '"TODO"'


@bottle.get('/legal/tos.json')
def handler_legal_tos():
    bottle.response.content_type = 'application/json'
    return '"TODO"'


# # # Handlers: /analyze/


@bottle.put('/analyze/tags.json')
@require_size
@require_auth
@require_version
def handler_analyze_tags():
    return {'result': {}}


@bottle.put('/analyze/objects.json')
@require_size
@require_auth
@require_version
def handler_analyze_objects():
    return {'result': {}}


@bottle.put('/analyze/scene.json')
@require_size
@require_auth
@require_version
def handler_analyze_scene():
    return {'result': {}}


@bottle.put('/analyze/location.json')
@require_size
@require_auth
@require_version
def handler_analyze_location():
    return {'result': {}}


@bottle.put('/analyze/time.json')
@require_size
@require_auth
@require_version
def handler_analyze_time():
    return {'result': {}}


@bottle.put('/analyze/faces.json')
@require_size
@require_auth
@require_version
def handler_analyze_faces():
    return {'result': {}}


@bottle.put('/analyze/rotate.json')
@require_size
@require_auth
@require_version
def handler_analyze_rotate():
    return {'result': {}}


@bottle.put('/analyze/segments.json')
@require_size
@require_auth
@require_version
def handler_analyze_segments():
    return {'result': {}}


# # # Handlers: /query/


@bottle.put('/query/similar.json')
@require_size
@require_auth
@require_version
def handler_query_similar():
    return {'result': {}}


# # # Handlers: /process/


@bottle.put('/process/info.json')
@require_size
@require_auth
@require_version
def handler_process_info():
    return {'result': {}}


@bottle.put('/process/register.json')
@require_size
@require_auth
@require_version
def handler_process_register():
    return {'result': {}}


@bottle.put('/process/convert.json')
@require_size
@require_auth
@require_version
def handler_process_convert():
    return {'result': {}}


@bottle.put('/process/cluster.json')
@require_size
@require_auth
@require_version
def handler_process_cluster():
    return {'result': {}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take in visual data")
    parser.add_argument('--port', type=str, help='Run on this port (default 8080)',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
    
