from gevent import monkey
monkey.patch_all()
import json
import bottle
import os
import argparse
import gevent.queue
import base64
import time
import hadoopy_hbase
import cPickle as pickle
import numpy as np
import gevent
import crawlers
import hashlib
import multiprocessing
from users import Users, UnknownUser
from yubikey import Yubikey
import picarus._features
from picarus._importer import call_import
from driver import PicarusManager
import logging
import uuid
import contextlib
from flickr_keys import FLICKR_API_KEY, FLICKR_API_SECRET
logging.basicConfig(level=logging.DEBUG)

VERSION = 'a1'


def check_version(func):

    def inner(version, *args, **kw):
        if version != VERSION:
            bottle.abort(400)
        return func(*args, **kw)
    return inner


def verify_slice_permissions(prefixes, start_row, stop_row, permissions):
    permissions = set(permissions)
    prefixes = [x for x, y in prefixes.items() if set(y).issuperset(permissions)]
    for prefix in prefixes:
        if prefix == '':
            return
        # NOTE: Prevents rollover, minor limitation on prefix is that it must not end in \xff
        assert prefix[-1] != '\xff'
        prefix_start_row = prefix
        prefix_stop_row = prefix[:-1] + chr(ord(prefix[-1]) + 1)
        if start_row and prefix_start_row <= start_row < prefix_stop_row and stop_row and prefix_start_row <= stop_row <= prefix_stop_row:
            return
    bottle.abort(401)


def _verify_row_permissions(prefixes, row, permissions):
    permissions = set(permissions)
    prefixes = [x for x, y in prefixes.items() if set(y).issuperset(permissions)]
    for prefix in prefixes:
        if prefix == '':
            return
        # NOTE: Prevents rollover, minor limitation on prefix is that it must not end in \xff
        assert prefix[-1] != '\xff'
        prefix_start_row = prefix
        prefix_stop_row = prefix[:-1] + chr(ord(prefix[-1]) + 1)
        if row and prefix_start_row <= row < prefix_stop_row:
            return
    bottle.abort(401)


def _images_column_write_validate(column):
    if column == 'data:image':
        return
    if column.startswith('meta:'):
        return
    bottle.abort(403)


def _models_column_write_validate(column):
    if column in ('data:notes', 'data:tags'):
        return
    if column.startswith('user:'):
        return
    bottle.abort(403)


def _images_verify_row_permissions(thrift, _auth_user, row, permissions):
    _verify_row_permissions(_auth_user.image_prefixes, row, permissions)


def _models_verify_row_permissions(thrift, _auth_user, row, permissions):
    results = thrift.get('picarus_models', row, 'user:' + _auth_user.email)
    if not results:
        bottle.abort(403)
    if not results[0].value.startswith(permissions):
        bottle.abort(403)


def _users_verify_row_permissions(thrift, _auth_user, row, permissions):
    if permissions == 'r' and row != _auth_user.email:
        bottle.abort(403)


TABLES = {'images': {'hbase_table': 'images', 'column_write_validator': _images_column_write_validate, 'verify_row_permissions': _images_verify_row_permissions},
          'models': {'hbase_table': 'picarus_models', 'column_write_validator': _models_column_write_validate, 'verify_row_permissions': _models_verify_row_permissions},
          'users': {'hbase_table': None, 'verify_row_permissions': _users_verify_row_permissions},
          'parameters': {'hbase_table': None, 'verify_row_permissions': None}}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Picarus REST Frontend')
    parser.add_argument('--users_redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--users_redis_port', type=int, help='Redis Port', default=6380)
    parser.add_argument('--users_redis_db', type=int, help='Redis DB', default=0)
    parser.add_argument('--yubikey_redis_host', help='Redis Host', default='localhost')
    parser.add_argument('--yubikey_redis_port', type=int, help='Redis Port', default=6380)
    parser.add_argument('--yubikey_redis_db', type=int, help='Redis DB', default=1)

    parser.add_argument('--port', default='15000', type=int)
    parser.add_argument('--thrift_server', default='localhost')
    parser.add_argument('--thrift_port', default='9090')
    ARGS = parser.parse_args()
    THRIFT_POOL = gevent.queue.Queue()
    THRIFT_CONSTRUCTOR = lambda : hadoopy_hbase.connect(ARGS.thrift_server, ARGS.thrift_port)
    for x in range(10):
        THRIFT_POOL.put(THRIFT_CONSTRUCTOR())
    USERS = Users(ARGS.users_redis_host, ARGS.users_redis_port, ARGS.users_redis_db)
    YUBIKEY = Yubikey(ARGS.yubikey_redis_host, ARGS.yubikey_redis_port, ARGS.yubikey_redis_db)
    #manager = PicarusManager(thrift=THRIFT)


@contextlib.contextmanager
def thrift_lock():
    try:
        cur_thrift = THRIFT_POOL.get()
        # When using thrift connection, detect if it is broken if so try one more time by making a new one
        yield cur_thrift
    finally:
        THRIFT_POOL.put(cur_thrift)


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
    if bottle.request.content_type == "application/json":
        return {str(k): str(v) for k, v in bottle.request.json.items()}, files
    for x in set(bottle.request.params) - set(bottle.request.files):
        params[x] = bottle.request.params[x]
    return params, files


def parse_columns():
    columns = {}
    if bottle.request.content_type == "application/json":
        columns = bottle.request.json['columns']
    else:
        columns = bottle.request.params.getall('column')
    return sorted((base64.urlsafe_b64decode(str(x)) for x in columns))


def parse_params():
    if bottle.request.content_type == "application/json":
        return {str(k): str(v) for k, v in bottle.request.json.items()}
    return dict(bottle.request.params)


# /data/:table


@bottle.get('/<version:re:[^/]+>/data/<table:re:[^/]+>')
@bottle.post('/<version:re:[^/]+>/data/<table:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_table(_auth_user, table):
    print_request()
    table_raw = table
    table_props = TABLES[table]
    table = table_props['hbase_table']
    method = bottle.request.method.upper()
    with thrift_lock() as thrift:
        if method == 'GET':
            columns = parse_columns()
            if table_raw == 'parameters':
                bottle.response.headers["Content-type"] = "application/json"
                columns = set(columns)
                if columns:
                    return json.dumps([{y: x[y] for y in columns.intersection(x)} for x in PARAM_SCHEMAS_B64])
                else:
                    return json.dumps(PARAM_SCHEMAS_B64)
            elif table_raw == 'models':
                user_column = 'user:' + _auth_user.email
                output_user = user_column in columns or not columns or 'user:' in columns
                hbase_filter = "SingleColumnValueFilter ('user', '%s', =, 'binaryprefix:r', true, true)" % _auth_user.email
                outs = []
                verify_row_permissions = lambda x: table_props['verify_row_permissions'](thrift, _auth_user, row, x)
                for row, cols in hadoopy_hbase.scanner(thrift, table, columns=columns + [user_column], filter=hbase_filter):
                    verify_row_permissions('r')
                    if not output_user:
                        del cols[user_column]
                    cur_out = {base64.urlsafe_b64encode(k): base64.b64encode(v) for k, v in cols.items()}
                    cur_out['row'] = base64.urlsafe_b64encode(row)
                    outs.append(cur_out)
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps(outs)
            else:
                bottle.abort(403)
        elif method == 'POST':
            if table_raw == 'images':
                verify_row_permissions = lambda x: table_props['verify_row_permissions'](thrift, _auth_user, row, x)
                prefix = _auth_user.upload_row_prefix
                row = prefix + '%.10d%s' % (2147483648 - int(time.time()), uuid.uuid4().bytes)
                verify_row_permissions('rw')
                mutations = []
                # NOTE: PATCH does the same operation, look into combining their logic
                params, files = parse_params_files()
                for x, y in files.items():
                    cur_column = base64.urlsafe_b64decode(x)
                    table_props['column_write_validator'](cur_column)
                    thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=cur_column, value=y.file.read())])
                for x, y in params.items():
                    cur_column = base64.urlsafe_b64decode(x)
                    table_props['column_write_validator'](cur_column)
                    mutations.append(hadoopy_hbase.Mutation(column=cur_column, value=base64.b64decode(y)))
                if mutations:
                    thrift.mutateRow(table, row, mutations)
                return {'row': base64.urlsafe_b64encode(row)}
            elif table_raw == 'models':
                path = params['path']
                manager = PicarusManager(thrift=thrift)
                return _create_model_from_params(manager, _auth_user, path, lambda model_dict, model_params, inputs: model_dict, params)
        else:
            bottle.abort(403)


def _user_to_dict(user):
    cols = {'stats': json.dumps(user.stats()), 'upload_row_prefix': user.upload_row_prefix, 'image_prefixes': json.dumps(user.image_prefixes)}
    cols = {base64.urlsafe_b64encode(x) : base64.b64encode(y) for x, y in cols.items()}
    cols['row'] = base64.urlsafe_b64encode(user.email)
    return cols

# /data/:table/:row

@bottle.route('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>', 'PATCH')
@bottle.post('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@bottle.delete('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@bottle.get('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_row(_auth_user, table, row):
    if table not in TABLES:
        bottle.abort(400)
    if not (table and row):
        bottle.abort(400)
    print_request()
    table_raw = table
    table_props = TABLES[table]
    table = table_props['hbase_table']
    params, files = parse_params_files()
    with thrift_lock() as thrift:
        verify_row_permissions = lambda x: table_props['verify_row_permissions'](thrift, _auth_user, row, x)
        manager = PicarusManager(thrift=thrift)
        row = base64.urlsafe_b64decode(row)
        method = bottle.request.method.upper()
        if method == 'GET':
            verify_row_permissions('r')
            if table_raw == 'users':
                if _auth_user.email != row:
                    bottle.abort(401)
                return _user_to_dict(_auth_user)
            columns = parse_columns()
            if columns:
                result = thrift.getRowWithColumns(table, row, columns)
            else:
                result = thrift.getRow(table, row)
            if not result:
                bottle.abort(404)
            return {base64.urlsafe_b64encode(x): base64.b64encode(y.value)
                    for x, y in result[0].columns.items()}
        elif method == 'PATCH':
            verify_row_permissions('rw')
            mutations = []
            for x, y in files.items():
                cur_column = base64.urlsafe_b64decode(x)
                table_props['column_write_validator'](cur_column)
                thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=cur_column, value=y.file.read())])
            print(params)
            for x, y in params.items():
                cur_column = base64.urlsafe_b64decode(x)
                table_props['column_write_validator'](cur_column)
                mutations.append(hadoopy_hbase.Mutation(column=cur_column, value=base64.b64decode(y)))
            if mutations:
                thrift.mutateRow(table, row, mutations)
            return {}
        elif method == 'POST':
            if table != 'images':
                bottle.abort(403)
            action = params['action']
            image_column = base64.urlsafe_b64decode(params['imageColumn'])
            results = thrift.get(table, row, image_column)
            if not results:
                bottle.abort(404)
            if action == 'i/classify':
                verify_row_permissions('r')
                classifier = _classifier_from_key(manager, base64.urlsafe_b64decode(params['model']))
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps(classifier(results[0].value))
            elif action == 'i/search':
                verify_row_permissions('r')
                index = _index_from_key(manager, base64.urlsafe_b64decode(params['model']))
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps(index(results[0].value))
            else:
                bottle.abort(400)
        elif method == 'DELETE':
            verify_row_permissions('rw')
            thrift.deleteAllRow(table, row)
            return {}
        else:
            bottle.abort(400)

# /data/:table/:row/:column

@bottle.delete('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>/<col:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_row_col(_auth_user, table, row, col):
    if table not in TABLES:
        bottle.abort(400)
    if not (table and row and col):
        bottle.abort(400)
    table_props = TABLES[table]
    table = table_props['hbase_table']
    with thrift_lock() as thrift:
        verify_row_permissions = lambda x: table_props['verify_row_permissions'](thrift, _auth_user, row, x)
        row = base64.urlsafe_b64decode(row)
        verify_row_permissions('rw')
        col = base64.urlsafe_b64decode(col)
        thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=col, isDelete=True)])
        return {}


SCANNER_CACHE = {}  # [(start_row, end_row, col, max_rows, cursor, user)] = scannerID


@bottle.post('/<version:re:[^/]*>/slice/<table:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>')
@bottle.route('/<version:re:[^/]*>/slice/<table:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>', 'PATCH')
@bottle.get('/<version:re:[^/]*>/slice/<table:re:[^/]+>/<start_row:re:[^/]+>/<stop_row:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_slice(_auth_user, table, start_row, stop_row):
    print_request()
    with thrift_lock() as thrift:
        manager = PicarusManager(thrift=thrift)
        start_row = base64.urlsafe_b64decode(start_row)
        stop_row = base64.urlsafe_b64decode(stop_row)
        method = bottle.request.method.upper()
        params, files = parse_params_files()
        columns = parse_columns()
        if table not in ('images',):
            bottle.abort(403)
        if method == 'GET':
            verify_slice_permissions(_auth_user.image_prefixes, start_row, stop_row, 'r')
            max_rows = min(100, int(params.get('maxRows', 1)))
            filter_string = params.get('filter')
            print('filter string[%s]' % filter_string)
            exclude_start = bool(int(params.get('excludeStart', 0)))
            cursor = params.get('cacheKey', '')
            scanner_key_func = lambda x, y: (x, y, tuple(columns), max_rows, cursor, filter_string, _auth_user.email)
            scanner_key = scanner_key_func(start_row, stop_row)
            try:
                if not exclude_start or not cursor:
                    raise KeyError
                scanner_id = SCANNER_CACHE[scanner_key]
                print('Reusing cached scanner [%s]' % str(scanner_key))  # TODO: Keep stats on this
                del SCANNER_CACHE[scanner_key]
                exclude_start = False
            except KeyError:
                scanner_id = hadoopy_hbase.scanner_create_id(thrift, table, columns=columns,
                                                             start_row=start_row, stop_row=stop_row, filter=filter_string)
            scanner = hadoopy_hbase.scanner_from_id(thrift, table, scanner_id, per_call=max_rows, close=False)
            stopped_early = False
            out = []
            cur_row = start_row
            for row_num, (cur_row, cur_columns) in enumerate(scanner, 1):
                if exclude_start and row_num == 1:
                    continue
                cur_out = {base64.urlsafe_b64encode(k): base64.b64encode(v) for k, v in cur_columns.items()}
                cur_out['row'] = base64.urlsafe_b64encode(cur_row)
                out.append(cur_out)
                if len(out) >= max_rows:
                    stopped_early = True
                    break
            if stopped_early and cursor:
                scanner_key = scanner_key_func(cur_row, stop_row)
                SCANNER_CACHE[scanner_key] = scanner_id
            bottle.response.headers["Content-type"] = "application/json"
            return json.dumps(out)
        elif method == 'PATCH':
            verify_slice_permissions(_auth_user.image_prefixes, start_row, stop_row, 'w')
            # NOTE: This only fetches rows that have a column in data: (it is a significant optimization)
            # NOTE: Only parameters allowed, no "files" due to memory restrictions
            mutations = []
            params = parse_params()
            for x, y in params.items():
                mutations.append(hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=base64.b64decode(y)))
            if mutations:
                for row, _ in hadoopy_hbase.scanner(thrift, table, start_row=start_row, stop_row=stop_row, filter='KeyOnlyFilter()', columns=['data:']):
                    thrift.mutateRow(table, row, mutations)
            return {}
        elif method == 'POST':
            action = params['action']
            if action == 'io/thumbnail':
                verify_slice_permissions(_auth_user.image_prefixes, start_row, stop_row, 'rw')
                print('Running thumb')
                manager.image_thumbnail(start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/exif':
                verify_slice_permissions(_auth_user.image_prefixes, start_row, stop_row, 'rw')
                print('Running exif')
                manager.image_exif(start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/preprocess':
                verify_slice_permissions(_auth_user.image_prefixes, start_row, stop_row, 'rw')
                print('Running preprocessor')
                manager.image_preprocessor(base64.urlsafe_b64decode(params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/classify':
                verify_slice_permissions(_auth_user.image_prefixes, start_row, stop_row, 'rw')
                print('Running classifier')
                manager.feature_to_prediction(base64.urlsafe_b64decode(params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/feature':
                verify_slice_permissions(_auth_user.image_prefixes, start_row, stop_row, 'rw')
                print('Running feature')
                manager.image_to_feature(base64.urlsafe_b64decode(params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/hash':
                verify_slice_permissions(_auth_user.image_prefixes, start_row, stop_row, 'rw')
                print('Running hash')
                manager.feature_to_hash(base64.urlsafe_b64decode(params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'i/dedupe/identical':
                col = base64.urlsafe_b64decode(params['column'])
                features = {}
                dedupe_feature = lambda x, y: features.setdefault(base64.b64encode(hashlib.md5(y).digest()), []).append(base64.urlsafe_b64encode(x))
                print('Running dedupe')
                for cur_row, cur_col in hadoopy_hbase.scanner_row_column(thrift, table, column=col,
                                                                         start_row=start_row, per_call=10,
                                                                         stop_row=stop_row):
                    dedupe_feature(cur_row, cur_col)
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps([{'rows': y} for x, y in features.items() if len(y) > 1])
            elif action == 'o/crawl/flickr':
                verify_slice_permissions(_auth_user.image_prefixes, start_row, stop_row, 'w')
                # Only slices where the start_row can be used as a prefix may be used
                assert start_row and ord(start_row[-1]) != 255 and start_row[:-1] + chr(ord(start_row[-1]) + 1) == stop_row
                print('Running flickr')
                p = {}
                row_prefix = start_row
                assert row_prefix.find(':') != -1
                class_name = params['className']
                query = params.get('query')
                query = class_name if query is None else query
                p['lat'] = query = params.get('lat')
                p['lon'] = query = params.get('lon')
                p['radius'] = query = params.get('radius')
                p['api_key'] = params.get('apiKey', FLICKR_API_KEY)
                p['api_secret'] = params.get('apiSecret', FLICKR_API_SECRET)
                if 'hasGeo' in params:
                    p['has_geo'] = params['hasGeo'] == '1'
                try:
                    p['min_upload_date'] = int(params['minUploadDate'])
                except KeyError:
                    pass
                try:
                    p['max_upload_date'] = int(params['maxUploadDate'])
                except KeyError:
                    pass
                try:
                    p['page'] = int(params['page'])
                except KeyError:
                    pass
                return {'data': {'numRows': crawlers.flickr_crawl(crawlers.HBaseCrawlerStore(thrift, row_prefix), class_name, query, **p)}}
            elif action in ('io/annotate/image/query', 'io/annotate/image/entity', 'io/annotate/image/query_batch'):
                global MTURK_SERVER
                if MTURK_SERVER is not None:
                    bottle.abort(500)  # Need to garbage collect these
                secret = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]
                p = {}
                image_column = base64.urlsafe_b64decode(params['imageColumn'])
                if action == 'io/annotate/image/entity':
                    entity_column = base64.urlsafe_b64decode(params['entityColumn'])
                    p['data'] = 'hbase://localhost:9090/images/%s/%s?entity=%s&image=%s' % (start_row, stop_row, entity_column, image_column)
                    p['type'] = 'image_entity'
                elif action == 'io/annotate/image/query':
                    query = params['query']
                    p['data'] = 'hbase://localhost:9090/images/%s/%s?image=%s' % (start_row, stop_row, image_column)
                    p['type'] = 'image_query'
                    p['query'] = query
                elif action == 'io/annotate/image/query_batch':
                    query = params['query']
                    p['data'] = 'hbase://localhost:9090/images/%s/%s?image=%s' % (start_row, stop_row, image_column)
                    p['type'] = 'image_query_batch'
                    p['query'] = query
                else:
                    bottle.abort(400)
                p['redis_address'] = 'localhost'
                p['redis_port'] = 6382
                p['port'] = 16000
                p['num_tasks'] = 100
                p['mode'] = 'standalone'
                p['setup'] = True
                p['reset'] = True
                p['secret'] = secret
                print(p)
                base_url = 'http://api0.picar.us:%d' % p['port']
                admin_prefix = '/admin/%s/' % secret
                MTURK_SERVER = multiprocessing.Process(target=_mturk_wrapper, kwargs=p)
                MTURK_SERVER.start()
                return {'worker': base_url, 'stop': base_url + admin_prefix + 'stop', 'results': base_url + admin_prefix + 'results.js', 'users': base_url + admin_prefix + 'users.js'}
            elif action.startswith('i/train/'):
                path = action[8:]
                
                def classifier_sklearn(model_dict, model_param, inputs):
                    row_cols = hadoopy_hbase.scanner(thrift, table,
                                                     columns=[inputs['feature'], inputs['meta']], start_row=start_row, stop_row=stop_row)
                    label_features = {0: [], 1: []}
                    for row, cols in row_cols:
                        label = int(cols[inputs['meta']] == model_param['class_positive'])
                        label_features[label].append(cols[inputs['feature']])
                    labels = [0] * len(label_features[0]) + [1] * len(label_features[1])
                    features = label_features[0] + label_features[1]
                    features = np.asfarray([picarus.api.np_fromstring(x) for x in features])
                    classifier = call_import(model_dict)
                    classifier.fit(features, np.asarray(labels))
                    return classifier

                def classifier_class_distance_list(model_dict, model_param, inputs):
                    row_cols = hadoopy_hbase.scanner(thrift, table,
                                                     columns=[inputs['multi_feature'], inputs['meta']], start_row=start_row, stop_row=stop_row)
                    #label_values = ((cols[inputs['meta']], np.asfarray(picarus.api.np_fromstring(cols[inputs['multi_feature']]))) for _, cols in row_cols)
                    def gen():
                        for _, cols in row_cols:
                            yield cols[inputs['meta']], np.asfarray(picarus.api.np_fromstring(cols[inputs['multi_feature']]))
                    classifier = call_import(model_dict)
                    classifier.train(gen()) # label_values
                    return classifier

                def hasher_train(model_dict, model_param, inputs):
                    hasher = call_import(model_dict)
                    features = hadoopy_hbase.scanner_column(thrift, table, inputs['feature'],
                                                            start_row=start_row, stop_row=stop_row)
                    return hasher.train(picarus.api.np_fromstring(x) for x in features)

                def index_train(model_dict, model_param, inputs):
                    index = call_import(model_dict)
                    row_cols = hadoopy_hbase.scanner(thrift, table,
                                                     columns=[inputs['hash'], inputs['meta']], start_row=start_row, stop_row=stop_row)
                    metadata, hashes = zip(*[(json.dumps([cols[inputs['meta']], base64.urlsafe_b64encode(row)]), cols[inputs['hash']])
                                             for row, cols in row_cols])
                    hashes = np.ascontiguousarray(np.asfarray([np.fromstring(h, dtype=np.uint8) for h in hashes]))
                    index = index.store_hashes(hashes, np.arange(len(metadata), dtype=np.uint64))
                    index.metadata = metadata
                    return index

                def kmeans_cluster_mfeat(model_dict, model_param, inputs):
                    # TODO: This needs to be finished, determine if we want quantizer level or cluster level
                    clusterer = call_import(model_dict)
                    features = []
                    row_cols = hadoopy_hbase.scanner(thrift, table,
                                                     columns=[inputs['multi_feature']], start_row=start_row, stop_row=stop_row)
                    # TODO: We'll want to check that we aren't clustering too much data by placing constraints
                    for row, columns in row_cols:
                        features.append(picarus.api.np_fromstring(columns[inputs['multi_feature']]))
                    features = np.vstack(features)
                    return clusterer.cluster(features)

                print(path)
                if path == 'classifier/svmlinear':
                    return _create_model_from_params(manager, _auth_user, path, classifier_sklearn, params)
                elif path == 'classifier/nbnnlocal':
                    return _create_model_from_params(manager, _auth_user, path, classifier_class_distance_list, params)
                elif path == 'hasher/rrmedian':
                    return _create_model_from_params(manager, _auth_user, path, hasher_train, params)
                elif path == 'index/linear':
                    return _create_model_from_params(manager, _auth_user, path, index_train, params)
                else:
                    bottle.abort(400)
            else:
                bottle.abort(400)
        else:
            bottle.abort(400)


def _classifier_from_key(manager, key):
    input, classifier, param = manager.key_to_input_model_param(key)
    if param['classifier_type'] == 'sklearn_decision_func':
        real_classifier = lambda x: float(classifier.decision_function(x).flat[0])
        input, feature, param = manager.key_to_input_model_param(input['feature'])
    else:
        real_classifier = classifier
        input, feature, param = manager.key_to_input_model_param(input['multi_feature'])
    loader = lambda x: call_import(x) if isinstance(x, dict) else x
    feature = loader(feature)
    if param['feature_type'] == 'multi_feature':
        real_feature = lambda x: feature.compute_dense(x)
    else:
        real_feature = feature
    input, preprocessor, param = manager.key_to_input_model_param(input['processed_image'])
    preprocessor = loader(preprocessor)
    return lambda x: real_classifier(real_feature(preprocessor.asarray(x)))


def _index_from_key(manager, key):
    loader = lambda x: call_import(x) if isinstance(x, dict) else x
    input, index, param = manager.key_to_input_model_param(key)
    input, hasher, param = manager.key_to_input_model_param(input['hash'])
    hasher = loader(hasher)
    input, feature, param = manager.key_to_input_model_param(input['feature'])
    feature = loader(feature)
    input, preprocessor, param = manager.key_to_input_model_param(input['processed_image'])
    preprocessor = loader(preprocessor)
    return lambda x: [json.loads(index.metadata[y]) for y in index.search_hash_knn(hasher(feature(preprocessor.asarray(x))).ravel(), 10)]


def _get_texton(manager):
    forests = []
    threshs = [0.]
    for x in ['outdoor', 'indoor']:
        tp = pickle.load(open('tree_ser-%s-texton.pkl' % x))
        tp2 = pickle.load(open('tree_ser-%s-integral.pkl' % x))
        forests.append({'tp': tp, 'tp2': tp2})
    return picarus._features.TextonILPPredict(num_classes=8, ilp=manager.key_to_classifier_pb('pred:h\x90\xf57\\\x8az\x0f\xd0K\xb6\xbc\xd7\taG\xa61l\x9b').SerializeToString(),
                                              forests=forests, threshs=threshs)




# [name]: {module, params}  where params is dict with "name" as key with value {'required': bool, type: (int or float), min, max} with [min, max) or {'required': bool, type: 'bool'} or {'required': enum, vals: [val0, val1, ...]}
PARAM_SCHEMAS = []
PARAM_SCHEMAS.append({'name': 'preprocessor',
                      'type': 'preprocessor',
                      'module': 'imfeat.ImagePreprocessor',
                      'data': 'none',   # none, row, slice
                      'inputs': ['raw_image'],  # abstract columns to be used for input
                      'model_params': {},
                      'module_params': {'compression': {'type': 'enum', 'values': ['jpg']},
                                       'size': {'type': 'int', 'min': 32, 'max': 1025},
                                       'method': {'type': 'enum', 'values': ['force_max_side', 'max_side', 'force_square']}}})

PARAM_SCHEMAS.append({'name': 'histogram',
                      'type': 'feature',
                      'data': 'none',
                      'inputs': ['processed_image'],
                      'module': 'imfeat.Histogram',
                      'model_params': {'feature_type': {'type': 'const', 'value': 'feature'}},
                      'module_params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                           'hsv', 'luv', 'hls', 'lab', 'gray']},
                                       'num_bins': {'type': 'int', 'min': 1, 'max': 17},
                                       'style': {'type': 'enum', 'values': ['joint', 'planar']}}})

PARAM_SCHEMAS.append({'name': 'svmlinear',
                      'type': 'classifier',
                      'data': 'slice',
                      'inputs': ['feature', 'meta'],
                      'module': 'sklearn.svm.LinearSVC',
                      'model_params': {'class_positive': {'type': 'str'}, 'classifier_type': {'type': 'const', 'value': 'sklearn_decision_func'}},
                      'module_params': {}})

PARAM_SCHEMAS.append({'name': 'rrmedian',
                      'type': 'hasher',
                      'data': 'slice',
                      'inputs': ['feature'],
                      'module': 'image_search.RRMedianHasher',
                      'model_params': {},
                      'module_params': {'hash_bits': {'type': 'int', 'min': 1, 'max': 513}, 'normalize_features': {'type': 'const', 'value': False}}})


PARAM_SCHEMAS.append({'name': 'linear',
                      'type': 'index',
                      'data': 'slice',
                      'inputs': ['hash', 'meta'],
                      'module': 'image_search.LinearHashDB',
                      'model_params': {},
                      'module_params': {}})


PARAM_SCHEMAS.append({'name': 'imageblocks',
                      'type': 'multi_feature',
                      'data': 'none',
                      'inputs': ['processed_image'],
                      'module': 'picarus.modules.ImageBlocks',
                      'model_params': {'feature_type': {'type': 'const', 'value': 'multi_feature'}},
                      'module_params': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                            'hsv', 'luv', 'hls', 'lab', 'gray']},
                                        'num_sizes': {'type': 'int', 'min': 1, 'max': 5},
                                        'sbin': {'type': 'int', 'min': 8, 'max': 257}}})

PARAM_SCHEMAS.append({'name': 'nbnnlocal',
                      'type': 'classifier',
                      'data': 'slice',
                      'inputs': ['multi_feature', 'meta'],
                      'module': 'picarus.modules.LocalNBNNClassifier',
                      'model_params': {'classifier_type': {'type': 'const', 'value': 'class_distance_list'}},
                      'module_params': {}})


for x in PARAM_SCHEMAS:
    x['path'] = '/'.join([x['type'], x['name']])
    x['prefix'] = {'feature': 'feat:', 'preprocessor': 'data:', 'classifier': 'pred:', 'hasher': 'hash:', 'index': 'srch:', 'multi_feature': 'mfeat:'}[x['type']]

PARAM_SCHEMAS_B64 = []
for schema in PARAM_SCHEMAS:
    cur_schema = dict(schema)
    cur_path = cur_schema['path']
    cur_schema = {base64.urlsafe_b64encode(x) : base64.b64encode(y) if isinstance(y, str) else base64.b64encode(json.dumps(y)) for x, y in cur_schema.items() if x != 'path'}
    cur_schema['row'] = cur_path
    PARAM_SCHEMAS_B64.append(cur_schema)

PARAM_SCHEMAS_SERVE = {}
for schema in PARAM_SCHEMAS:
    PARAM_SCHEMAS_SERVE[schema['path']] = dict(schema)


def _parse_model_params(params, schema, prefix):
    kw = {}
    schema_params = schema[prefix + '_params']
    get_param = lambda x: params[prefix + '-' + x]
    for param_name, param in schema_params.items():
        if param['type'] == 'enum':
            param_value = get_param(param_name)
            if param_value not in param['values']:
                bottle.abort(400)
            kw[param_name] = param_value
        elif param['type'] == 'int':
            param_value = int(get_param(param_name))
            if not (param['min'] <= param_value < param['max']):
                bottle.abort(400)
            kw[param_name] = param_value
        elif param['type'] == 'const':
            kw[param_name] = param['value']
        elif param['type'] == 'str':
            kw[param_name] = get_param(param_name)
        else:
            bottle.abort(400)
    return kw


def _create_model_from_params(manager, _auth_user, path, create_model, params):
    try:
        schema = PARAM_SCHEMAS_SERVE[path]
        model_params = _parse_model_params(params, schema, 'model')
        module_params = _parse_model_params(params, schema, 'module')
        model_dict = {'name': schema['module'], 'kw': module_params}
        get_key = lambda x: base64.urlsafe_b64decode(params['key-' + x])   # TODO: Verify that model keys exist
        prefix = {'feature': 'feat:', 'preprocessor': 'data:', 'classifier': 'pred:', 'hasher': 'hash:', 'index': 'srch:', 'multi_feature': 'mfeat:'}[schema['type']]
        inputs = {x: get_key(x) for x in schema['inputs']}
        model = create_model(model_dict, model_params, inputs)
        row = manager.input_model_param_to_key(prefix, input=inputs, model=model, email=_auth_user.email, name=manager.model_to_name(model_dict), param=model_params)
        return {'row': base64.urlsafe_b64encode(row)}
    except ValueError:
        bottle.abort(500)


@bottle.get('/static/<name:re:[^/]+>')
def static(name):
    return bottle.static_file(name, root=os.path.join(os.getcwd(), 'static'))


@bottle.get('/robots.txt')
def robots():
    return '''User-agent: *
Disallow: /'''


@bottle.post('/<version:re:[^/]*>/auth/email')
@check_version
@USERS.auth_login_key(True)
def auth_email(_auth_user):
    try:
        USERS.email_api_key(_auth_user)
    except UnknownUser:
        bottle.abort(401)
    return {}


@bottle.post('/<version:re:[^/]*>/auth/yubikey')
@check_version
@USERS.auth_login_key(True)
def auth_yubikey(_auth_user):
    print_request()
    params = parse_params()
    try:
        email = YUBIKEY.verify(params['otp'])
    except UnknownUser:
        bottle.abort(401)
    if not email or email != _auth_user.email:
        bottle.abort(401)
    return {'apiKey': _auth_user.create_api_key()}


MTURK_SERVER = None


def _mturk_wrapper(*args, **kw):
    bottle.app[0] = bottle.Bottle()  # Clear previous app
    import mturk_vision
    out = mturk_vision.server(*args, **kw)
    manager = PicarusManager(thrift=THRIFT_CONSTRUCTOR())
    if kw['type'] == 'image_query_batch':
        manager.filter_batch_annotations_to_hbase()
    else:
        manager.filter_annotations_to_hbase()
    return out

if __name__ == '__main__':
    import gevent.pywsgi
    SERVER = gevent.pywsgi.WSGIServer(('0.0.0.0', ARGS.port), bottle.app())
    SERVER.serve_forever()
