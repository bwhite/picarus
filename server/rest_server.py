#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()
import bottle
bottle.BaseRequest.MEMFILE_MAX = 10 * 1024 ** 2  # 10MB file cap
import argparse
import gevent.queue
import base64
import gevent
import mturk_vision
from users import Users, UnknownUser
from yubikey import Yubikey
from databases import HBaseDB, RedisDB
import jobs
import logging
import contextlib
import tables
import glob


def check_version(func):

    def func_raven(*args, **kw):
        try:
            return func(*args, **kw)
        except bottle.HTTPError:
            raise
        except:
            RAVEN.captureException()
            raise
    func2 = func_raven if ARGS.raven else func

    def inner(version, *args, **kw):
        if ARGS.debug:
            print_request()
        if version != VERSION:
            bottle.abort(400)
        return func2(*args, **kw)
    return inner


@contextlib.contextmanager
def thrift_lock():
    try:
        cur_thrift = THRIFT_POOL.get()
        yield cur_thrift
    finally:
        THRIFT_POOL.put(cur_thrift)


@contextlib.contextmanager
def thrift_new():
    yield THRIFT_CONSTRUCTOR()


def load_site():
    site = {}
    for x in glob.glob('static/*'):
        site[x] = open(x).read()
    return site


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Run Picarus REST Frontend')
    parser.add_argument('--redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--redis_port', type=int, help='Redis Port', default=6379)
    parser.add_argument('--annotations_redis_host', help='Annotations Host', default='localhost')
    parser.add_argument('--annotations_redis_port', type=int, help='Annotations Port', default=6380)
    parser.add_argument('--raven', help='URL to the Raven/Sentry logging server')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--port', default='80', type=int)
    parser.add_argument('--thrift_server', default='localhost')
    parser.add_argument('--thrift_port', default='9090')
    parser.add_argument('--database', choices=['hbase', 'redis'], help='Select which database to use as our backend')
    ARGS = parser.parse_args()
    if ARGS.raven:
        import raven
        RAVEN = raven.Client(ARGS.raven)
    THRIFT_POOL = gevent.queue.Queue()

    def THRIFT_CONSTRUCTOR():
        if ARGS.database == 'redis':
            return RedisDB(ARGS.redis_host, ARGS.redis_port, 2)
        if ARGS.database == 'hbase':
            return HBaseDB(ARGS.thrift_server, ARGS.thrift_port)
        raise ValueError('Unknown option[%s]' % ARGS.database)
    for x in range(5):
        THRIFT_POOL.put(THRIFT_CONSTRUCTOR())
    USERS = Users(ARGS.redis_host, ARGS.redis_port, 0)
    YUBIKEY = Yubikey(ARGS.redis_host, ARGS.redis_port, 1)
    JOBS = jobs.Jobs(ARGS.redis_host, ARGS.redis_port, 3, ARGS.annotations_redis_host, ARGS.annotations_redis_port)
    SITE = load_site()
    # Set necessary globals in tables module
    tables.VERSION = VERSION = 'v0'
    tables.thrift_lock = thrift_lock
    tables.thrift_new = thrift_new
    tables.JOBS = JOBS


def print_request():
    ks = ['auth', 'content_length', 'content_type', 'environ', 'fullpath', 'is_ajax', 'is_xhr', 'method', 'path', 'query_string', 'remote_addr', 'remote_route', 'script_name', 'url', 'urlparts']
    for k in ks:
        print('%s: %s' % (k, str(getattr(bottle.request, k))))

    print('%s: %s' % ('files', (getattr(bottle.request, 'files')).keys()))

    ks = ['forms', 'params', 'query', 'cookies', 'headers']
    for k in ks:
        print('%s: %s' % (k, str(dict(getattr(bottle.request, k)))))


def parse_params_files():
    params = {}
    files = {}
    for x in bottle.request.files:
        files[x] = bottle.request.files[x]
    if "application/json" in bottle.request.content_type:
        # TODO: Is this too strict?  We may want to let json expose real types
        return {str(k): str(v) for k, v in bottle.request.json.items()}, files
    for x in set(bottle.request.params) - set(bottle.request.files):
        params[x] = bottle.request.params[x]
    return params, files


def parse_columns():
    columns = {}
    if bottle.request.content_type == "application/json":
        columns = bottle.request.json['columns']
    else:
        try:
            columns = bottle.request.params['columns'].split(',')
        except KeyError:
            columns = []
    return [base64.b64decode(str(x)) for x in columns]


def parse_params():
    if bottle.request.content_type == "application/json":
        # TODO: Is this too strict?  We may want to let json expose real types
        return {str(k): str(v) for k, v in bottle.request.json.items()}
    return dict(bottle.request.params)


@bottle.get('/<version:re:[^/]+>/data/<table_name:re:[^/]+>')
@bottle.post('/<version:re:[^/]+>/data/<table_name:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_table(_auth_user, table_name):
    table = tables.get_table(_auth_user, table_name)
    method = bottle.request.method.upper()
    if method == 'GET':
        return table.get_table(columns=parse_columns())
    elif method == 'POST':
        return table.post_table(*parse_params_files())
    else:
        bottle.abort(403)


@bottle.route('/<version:re:[^/]*>/data/<table_name:re:[^/]+>/<row:re:[^/]+>', 'PATCH')
@bottle.post('/<version:re:[^/]*>/data/<table_name:re:[^/]+>/<row:re:[^/]+>')
@bottle.delete('/<version:re:[^/]*>/data/<table_name:re:[^/]+>/<row:re:[^/]+>')
@bottle.get('/<version:re:[^/]*>/data/<table_name:re:[^/]+>/<row:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_row(_auth_user, table_name, row):
    table = tables.get_table(_auth_user, table_name)
    method = bottle.request.method.upper()
    row = base64.urlsafe_b64decode(row)
    method = bottle.request.method.upper()
    if method == 'GET':
        return table.get_row(row, parse_columns())
    elif method == 'PATCH':
        return table.patch_row(row, *parse_params_files())
    elif method == 'POST':
        return table.post_row(row, *parse_params_files())
    elif method == 'DELETE':
        return table.delete_row(row)
    else:
        bottle.abort(403)


@bottle.delete('/<version:re:[^/]*>/data/<table_name:re:[^/]+>/<row:re:[^/]+>/<column:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_column(_auth_user, table_name, row, column):
    table = tables.get_table(_auth_user, table_name)
    row = base64.urlsafe_b64decode(row)
    column = base64.urlsafe_b64decode(column)
    return table.delete_column(row, column)


@bottle.route('/<version:re:[^/]*>/slice/<table_name:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>', 'PATCH')
@bottle.post('/<version:re:[^/]*>/slice/<table_name:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>')
@bottle.delete('/<version:re:[^/]*>/slice/<table_name:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>')
@bottle.get('/<version:re:[^/]*>/slice/<table_name:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_slice(_auth_user, table_name, start_row, stop_row):
    table = tables.get_table(_auth_user, table_name)
    method = bottle.request.method.upper()
    start_row = base64.urlsafe_b64decode(start_row)
    stop_row = base64.urlsafe_b64decode(stop_row)
    if method == 'GET':
        return table.get_slice(start_row, stop_row, parse_columns(), *parse_params_files())
    elif method == 'PATCH':
        return table.patch_slice(start_row, stop_row, *parse_params_files())
    elif method == 'DELETE':
        return table.delete_slice(start_row, stop_row)
    elif method == 'POST':
        return table.post_slice(start_row, stop_row, *parse_params_files())
    else:
        bottle.abort(403)


@bottle.get('/static/<name:re:[^/]+>')
def static(name):
    try:
        bottle.response.headers['Cache-Control'] = 'public, max-age=3600, must-revalidate'
        if name.endswith('.js'):
            bottle.response.headers["Content-type"] = "application/javascript"
        elif name.endswith('.css'):
            bottle.response.headers["Content-type"] = "text/css"
        elif name.endswith('.png'):
            bottle.response.headers["Content-type"] = "image/png"
        elif name.endswith('.svg'):
            bottle.response.headers["Content-type"] = "image/svg+xml"
        return SITE['static/' + name]
    except KeyError:
        bottle.abort(404)


@bottle.get('/')
def index():
    try:
        bottle.response.headers['Cache-Control'] = 'public, max-age=3600, must-revalidate'
        return SITE['static/app.html']
    except KeyError:
        bottle.abort(404)


@bottle.get('/robots.txt')
def robots():
    return '''User-agent: *
Disallow: /'''


@bottle.post('/<version:re:[^/]*>/auth/email')
@check_version
@USERS.auth_login_key(True)
def auth_email(_auth_user):
    params = parse_params()
    try:
        USERS.email_api_key(_auth_user, ttl=params.get('ttl'))
    except UnknownUser:
        bottle.abort(401)
    return {}


@bottle.post('/<version:re:[^/]*>/auth/yubikey')
@check_version
@USERS.auth_login_key(True)
def auth_yubikey(_auth_user):
    params = parse_params()
    try:
        email = YUBIKEY.verify(params['otp'])
    except UnknownUser:
        bottle.abort(401)
    if not email or email != _auth_user.email:
        bottle.abort(401)
    return {'apiKey': _auth_user.create_api_key(ttl=params.get('ttl'))}


@bottle.get('/<version:re:[^/]*>/annotation/<task:re:[^/]*>/index.html')
@check_version
def annotate_index(task):
    try:
        return JOBS.get_annotation_manager(task).index
    except KeyError:
        bottle.abort(404)


@bottle.get('/<version:re:[^/]*>/annotation/<task:re:[^/]*>/static/:file_name')
@check_version
def annotation_static(task, file_name):
    try:
        JOBS.get_annotation_manager(task)
    except KeyError:
        bottle.abort(404)
    root = mturk_vision.__path__[0] + '/static'
    return bottle.static_file(file_name, root)


@bottle.get('/<version:re:[^/]*>/annotation/<task:re:[^/]*>/user.js')
@check_version
def annotation_user(task):
    try:
        return JOBS.get_annotation_manager(task).user(bottle.request)
    except KeyError:
        bottle.abort(404)


@bottle.get('/<version:re:[^/]*>/annotation/<task:re:[^/]*>/config.js')
@check_version
def annotation_config(task):
    try:
        return JOBS.get_annotation_manager(task).config
    except KeyError:
        bottle.abort(404)


@bottle.get('/<version:re:[^/]*>/annotation/<task:re:[^/]*>/:user_id/data.js')
@check_version
def annotation_data(task, user_id):
    try:
        return JOBS.get_annotation_manager(task).make_data(user_id)
    except KeyError:
        bottle.abort(404)


@bottle.get('/<version:re:[^/]*>/annotation/<task:re:[^/]*>/image/:image_key')
@check_version
def annotation_image_get(task, image_key):
    try:
        data_key = image_key.rsplit('.', 1)[0]
        cur_data = JOBS.get_annotation_manager(task).read_data(data_key)
    except KeyError:
        bottle.abort(404)
    bottle.response.content_type = "image/jpeg"
    return cur_data


@bottle.get('/<version:re:[^/]*>/annotation/<task:re:[^/]*>/data/:data_key')
@check_version
def annotation_data_get(task, data_key):
    try:
        cur_data = JOBS.get_annotation_manager(task).read_data(data_key)
    except KeyError:
        bottle.abort(404)
    return cur_data


@bottle.post('/<version:re:[^/]*>/annotation/<task:re:[^/]*>/result')
@check_version
def annotation_result(task):
    try:
        return JOBS.get_annotation_manager(task).result(**bottle.request.json)
    except KeyError:
        bottle.abort(404)


if __name__ == '__main__':
    import gevent.pywsgi
    SERVER = gevent.pywsgi.WSGIServer(('0.0.0.0', ARGS.port), bottle.app())
    SERVER.serve_forever()
