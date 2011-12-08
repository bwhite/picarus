import gevent
from gevent import monkey
monkey.patch_all()
import bottle
import argparse
import time
bottle.debug(True)
# Designed to be sent over HTTPS
# {"data": [{"type": "image", "binary_b64": "sdfskjdkfsjkjsd98sfskj"}], "query": {"nouns": ["car", "dog"]}, "version": {"major": 0, "minor": 0, "patch": 0}}


def auth(func):
    """Authentication decorator

    This verifies that the user is able to access the requested resource, handles
    error code reporting if not, populates an auth_funcs dictionary of functions
    requiring authentication (anything requiring priveleges must be used from here).
    """
    def inner(*args, **kw):
        if bottle.request.auth != ('user', 'pass'):
            bottle.abort(401)
        else:
            return func(auth_funcs={}, *args, **kw)
    return inner


# # # Handlers: /help/


@bottle.get('/help/test.json')
def handler_help_test():
    bottle.response.content_type = 'application/json'
    return '"ok"'


@bottle.get('/help/configuration.json')
def handler_help_configuration():
    bottle.response.content_type = 'application/json'
    return '"ok"'


@bottle.get('/help/status.json')
def handler_help_status():
    bottle.response.content_type = 'application/json'
    return '"ok"'


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
@auth
def handler_query_classify():
    print(bottle.request.auth)
    return {'result': {'nouns': ['car', 'dog']}}


@bottle.put('/query/detect.json')
@auth
def handler_query_detect():
    print(bottle.request.auth)
    return {'result': {'nouns': ['car', 'dog']}}


@bottle.put('/query/scene.json')
@auth
def handler_query_scene():
    print(bottle.request.auth)
    return {'result': {'nouns': ['car', 'dog']}}


@bottle.put('/query/search.json')
@auth
def handler_query_search():
    print(bottle.request.auth)
    return {'result': {'nouns': ['car', 'dog']}}


@bottle.put('/query/faces.json')
@auth
def handler_query_faces():
    print(bottle.request.auth)
    return {'result': {'nouns': ['car', 'dog']}}


@bottle.put('/query/rotated.json')
@auth
def handler_query_rotate():
    print(bottle.request.auth)
    return {'result': {'nouns': ['car', 'dog']}}


@bottle.put('/query/segment.json')
@auth
def handler_query_segment():
    print(bottle.request.auth)
    return {'result': {'nouns': ['car', 'dog']}}


@bottle.put('/query/info.json')
@auth
def handler_query_info():
    print(bottle.request.auth)
    return {'result': {'nouns': ['car', 'dog']}}


@bottle.put('/query/register.json')
@auth
def handler_query_register():
    print(bottle.request.auth)
    return {'result': {'nouns': ['car', 'dog']}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take in visual data")
    parser.add_argument('--port', type=str, help='Run on this port (default 8080)',
                        default='8080')
    ARGS = parser.parse_args()
    bottle.run(host='0.0.0.0', port=ARGS.port, server='gevent')
    
