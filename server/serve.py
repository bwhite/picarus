import gevent
from gevent import monkey
monkey.patch_all()
import bottle
import argparse
import time
import json
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


# # # Handlers: /query/

@bottle.put('/query/classify.json')
@require_size
@require_auth
@require_version
def handler_query_classify():
    return {'result': {}}


@require_version
@bottle.put('/query/detect.json')
@require_auth
def handler_query_detect():
    return {'result': {}}


@bottle.put('/query/scene.json')
@require_auth
@require_version
def handler_query_scene():
    return {'result': {}}


@bottle.put('/query/similar.json')
@require_auth
@require_version
def handler_query_similar():
    return {'result': {}}


@bottle.put('/query/location.json')
@require_auth
@require_version
def handler_query_location():
    return {'result': {}}


@bottle.put('/query/faces.json')
@require_auth
@require_version
def handler_query_faces():
    return {'result': {}}


@bottle.put('/query/rotated.json')
@require_auth
@require_version
def handler_query_rotate():
    return {'result': {}}


@bottle.put('/query/segmentation.json')
@require_auth
@require_version
def handler_query_segmentation():
    return {'result': {}}


# # # Handlers: /process/


@bottle.put('/process/info.json')
@require_auth
@require_version
def handler_query_info():
    return {'result': {}}


@bottle.put('/process/register.json')
@require_auth
@require_version
def handler_query_register():
    return {'result': {}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take in visual data")
    parser.add_argument('--port', type=str, help='Run on this port (default 8080)',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
    
