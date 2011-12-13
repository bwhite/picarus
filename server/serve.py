from gevent import monkey
monkey.patch_all()
import bottle
import argparse
import time
import json
import imfeat
import base64
import requests
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
            bottle.abort(401, 'Invalid username or password.')
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
        # Install routes for all specified methods
        for ext, return_conv in [('.json', return_json)]:
            methods = [method] if isinstance(method, str) else method
            for m in methods:
                if m.lower() == 'get':
                    bottle.route(route + ext, method=m)(return_conv(func))
                else:
                    bottle.route(route + ext, method=m)(return_conv(require_version(require_auth(require_size(func)))))
        return func
    return inner


def single_image_handler(mode_or_modes=None):
    if mode_or_modes is None:
        mode_or_modes = {'type': 'numpy', 'dtype': 'uint8', 'mode': 'bgr'}

    def inner0(func):

        def inner1():
            request = bottle.request.json
            if 'image' in request:
                if request['image']['type'] == 'b64':
                    image_data = base64.b64decode(request['image']['image_data'])
                elif request['image']['type'] == 'url':
                    image_data = requests.get(request['image']['url']).content
                else:
                    bottle.abort(400)
                result = func(imfeat.image_fromstring(image_data, mode_or_modes))
            else:
                bottle.abort(400)
            return result
        inner1.__name__ = func.__name__
        return inner1
    return inner0


def multi_image_handler():
    return lambda x: x


def multi_vector_handler():
    return lambda x: x


@bottle.error(400)
@bottle.error(401)
@bottle.error(403)
@bottle.error(404)
@bottle.error(414)
@bottle.error(500)
def error_handler(r):
    bottle.response.content_type = 'application/json'
    return json.dumps({'message': r.output})
    

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
@single_image_handler()
def see__tags(image):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def see__objects(image):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def see__scene(image):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def see__location(image):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def see__time(image):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def see__who(image):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def see__faces(image):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def see__orientation(image):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def see__segments(image):
    return {}


# # # Handlers: /query/

@register_with_underscores(method='put')
@single_image_handler()
def query__similar(image):
    return {}

# # # Handlers: /demo/


@bottle.get('/demo/all.html')
def demo__all():
    return bottle.static_file('demo_all.html', root='static/')


# # # Handlers: /

@register_with_underscores(method='put')
@single_image_handler()
def info(image):
    return {'height': image.shape[0],
            'width': image.shape[1]}


@register_with_underscores(method='put')
@multi_image_handler()
def register(images):
    return {}


@register_with_underscores(method='put')
@multi_image_handler()
def stabilize(images):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def convert(image):
    return {}


@register_with_underscores(method='put')
@multi_vector_handler()
def compute_clusters(vectors):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def compute_points(image):
    return {}


@register_with_underscores(method='put')
@single_image_handler()
def compute_features(image):
    return {}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take in visual data")
    parser.add_argument('--port', type=str, help='Run on this port (default 8080)',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
    
