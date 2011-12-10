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


def return_json(func):
    def inner(*args, **kw):
        bottle.response.content_type = 'application/json'
        return json.dumps(func(*args, **kw))
    return inner


def register_with_underscores(quality=0, doc='', author={}, url='', method='get'):

    def inner(func):
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

        route = '/'.join([''] + func.__name__.split('__'))
        for ext, return_conv in [('.json', return_json)]:
            methods = [method] if isinstance(method, str) else method
            for m in methods:
                if m.lower() == 'get':
                    bottle.route(route + ext, method=m)(return_conv(func))
                else:
                    bottle.route(route + ext, method=m)(return_conv(require_version(require_auth(require_size(func)))))
        return func
    return inner


# # # Handlers: /help/

@register_with_underscores(quality=3)
def help__test():
    return 'ok'


@register_with_underscores(quality=1)
def help__configuration():
    return {'version': SERVER_VERSION,
            'max_request_size': bottle.BaseRequest.MEMFILE_MAX,
            'time': time.time()}


@register_with_underscores(quality=1)
def help__status():
    return {}


# # # Handlers: /legal/

@register_with_underscores()
def legal__privacy():
    return 'TODO'


@register_with_underscores()
def legal__tos():
    return 'TODO'


# # # Handlers: /see/

@register_with_underscores(method='put')
def see__tags():
    return {'result': {}}


@register_with_underscores(method='put')
def see__objects():
    return {'result': {}}


@register_with_underscores(method='put')
def see__scene():
    return {'result': {}}


@register_with_underscores(method='put')
def see__location():
    return {'result': {}}


@register_with_underscores(method='put')
def see__time():
    return {'result': {}}


@register_with_underscores(method='put')
def see__who():
    return {'result': {}}


@register_with_underscores(method='put')
def see__faces():
    return {'result': {}}


@register_with_underscores(method='put')
def see__orientation():
    return {'result': {}}

@register_with_underscores(method='put')
def see__segments():
    return {'result': {}}


# # # Handlers: /query/

@register_with_underscores(method='put')
def query__similar():
    return {'result': {}}


# # # Handlers: /

@register_with_underscores(method='put')
def info():
    return {'result': {}}


@register_with_underscores(method='put')
def register():
    return {'result': {}}


@register_with_underscores(method='put')
def stabilize():
    return {'result': {}}


@register_with_underscores(method='put')
def convert():
    return {'result': {}}


@register_with_underscores(method='put')
def compute_clusters():
    return {'result': {}}


@register_with_underscores(method='put')
def compute_points():
    return {'result': {}}


@register_with_underscores(method='put')
def compute_features():
    return {'result': {}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take in visual data")
    parser.add_argument('--port', type=str, help='Run on this port (default 8080)',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
    
