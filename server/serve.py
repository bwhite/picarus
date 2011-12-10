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


def method_info(quality=0, doc='', author={}, url=''):

    def inner0(func):
        quality_codes = dict((x, [x, y]) for x, y in enumerate(['unimplemented', 'preliminary implementation',
                                                                'partial implementation', 'draft implementation',
                                                                'alpha implementation', 'beta implementation',
                                                                'production implementation']))
        info = {'quality': quality_codes[quality], 'handler_name': func.__name__}
        if doc:
            info['doc'] = doc
        if author:
            info['author'] = author
        if url:
            info['url'] = url

        def inner1(*args, **kw):
            out = func(*args, **kw)
            out['info'] = info
            return out
        return inner1
    return inner0


# # # Handlers: /help/

@bottle.get('/help/test.json')
@method_info(3)
def help_test():
    bottle.response.content_type = 'application/json'
    return {'result': 'ok'}


@bottle.get('/help/configuration.json')
@method_info(1)
def help_configuration():
    bottle.response.content_type = 'application/json'
    return {'version': SERVER_VERSION,
            'max_request_size': bottle.BaseRequest.MEMFILE_MAX,
            'time': time.time()}


@bottle.get('/help/status.json')
@method_info()
def help_status():
    bottle.response.content_type = 'application/json'
    return {}


# # # Handlers: /legal/

@bottle.get('/legal/privacy.json')
@method_info()
def legal_privacy():
    bottle.response.content_type = 'application/json'
    return {'result': 'TODO'}


@bottle.get('/legal/tos.json')
@method_info()
def legal_tos():
    bottle.response.content_type = 'application/json'
    return {'result': 'TODO'}


# # # Handlers: /see/

@bottle.put('/see/tags.json')
@require_size
@require_auth
@require_version
@method_info()
def see_tags():
    return {'result': {}}


@bottle.put('/see/objects.json')
@require_size
@require_auth
@require_version
@method_info()
def see_objects():
    return {'result': {}}


@bottle.put('/see/scene.json')
@require_size
@require_auth
@require_version
@method_info()
def see_scene():
    return {'result': {}}


@bottle.put('/see/location.json')
@require_size
@require_auth
@require_version
@method_info()
def see_location():
    return {'result': {}}


@bottle.put('/see/time.json')
@require_size
@require_auth
@require_version
@method_info()
def see_time():
    return {'result': {}}


@bottle.put('/see/who.json')
@require_size
@require_auth
@require_version
@method_info()
def see_who():
    return {'result': {}}


@bottle.put('/see/faces.json')
@require_size
@require_auth
@require_version
@method_info()
def see_faces():
    return {'result': {}}


@bottle.put('/see/rotate.json')
@require_size
@require_auth
@require_version
@method_info()
def see_rotate():
    return {'result': {}}


@bottle.put('/see/segments.json')
@require_size
@require_auth
@require_version
@method_info()
def see_segments():
    return {'result': {}}


# # # Handlers: /query/


@bottle.put('/query/similar.json')
@require_size
@require_auth
@require_version
@method_info()
def query_similar():
    return {'result': {}}


# # # Handlers: /


@bottle.put('/info.json')
@require_size
@require_auth
@require_version
@method_info()
def info():
    return {'result': {}}


@bottle.put('/register.json')
@require_size
@require_auth
@require_version
@method_info()
def register():
    return {'result': {}}


@bottle.put('/stabilize.json')
@require_size
@require_auth
@require_version
@method_info()
def stabilize():
    return {'result': {}}


@bottle.put('/convert.json')
@require_size
@require_auth
@require_version
@method_info()
def convert():
    return {'result': {}}


@bottle.put('/cluster.json')
@require_size
@require_auth
@require_version
@method_info()
def compute_clusters():
    return {'result': {}}


@bottle.put('/points.json')
@require_size
@require_auth
@require_version
@method_info()
def compute_points():
    return {'result': {}}


@bottle.put('/features.json')
@require_size
@require_auth
@require_version
@method_info()
def compute_features():
    return {'result': {}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take in visual data")
    parser.add_argument('--port', type=str, help='Run on this port (default 8080)',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
    
