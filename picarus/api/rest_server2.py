from gevent import monkey
monkey.patch_all()
import json
import mimerender
import bottle
import os
import argparse
import gevent.queue
import random
import base64
import imfeat
import time
import redis
import hadoopy_hbase
import cPickle as pickle
import numpy as np
import cv2
import gevent
import crawlers
import hashlib
import multiprocessing
import distpy
from users import Users, UnknownUser
from yubikey import Yubikey
from picarus.modules import HashRetrievalClassifier
import picarus._features
import boto
from picarus._importer import call_import
from driver import PicarusManager
import logging
import uuid
import contextlib
from flickr_keys import FLICKR_API_KEY, FLICKR_API_SECRET
import scipy as sp
import scipy.cluster.vq
logging.basicConfig(level=logging.DEBUG)

VERSION = 'a1'


def check_version(func):

    def inner(version, *args, **kw):
        if version != VERSION:
            bottle.abort(400)
        return func(*args, **kw)
    return inner


def verify_slice_permissions(prefixes, permissions, start_row, stop_row):
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


def verify_row_permissions(prefixes, permissions, row):
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


if __name__ == "__main__":
    mimerender = mimerender.BottleMimeRender()
    render_xml = lambda message: '<message>%s</message>'%message
    render_json = lambda **args: json.dumps(args)
    render_html = lambda message: '<html><body>%s</body></html>'%message
    render_txt = lambda message: message
    render_xml_exception = lambda exception: '<exception>%s</exception>' % exception.message
    render_json_exception = lambda exception: json.dumps({'exception': exception.message})

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


@bottle.get('/<version:re:[^/]*>/user')
@USERS.auth_api_key(True)
@check_version
def user_info(_auth_user):
    print(_auth_user.email)
    return {'stats': _auth_user.stats(), 'uploadRowPrefix': _auth_user.upload_row_prefix}


@bottle.post('/<version:re:[^/]*>/data/<table:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_row_upload(_auth_user, table):
    with thrift_lock() as thrift:
        prefix = _auth_user.upload_row_prefix
        row = prefix + '%.10d%s' % (2147483648 - int(time.time()), uuid.uuid4().bytes)
        verify_row_permissions(_auth_user.image_prefixes, 'w', row)
        mutations = []
        # TODO: Reuse PATCH code which also does this
        for x in bottle.request.files:
            thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=bottle.request.files[x].file.read())])
        for x in set(bottle.request.params) - set(bottle.request.files):
            print('ParmLen[%d]' % len(bottle.request.params[x]))
            print('md5[%s]' % hashlib.md5(bottle.request.params[x]).hexdigest())
            mutations.append(hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=bottle.request.params[x]))
        if mutations:
            thrift.mutateRow(table, row, mutations)
        return {'row': base64.urlsafe_b64encode(row)}


def _user_to_dict(user):
    return {'stats': user.stats(), 'uploadRowPrefix': user.upload_row_prefix, 'email': user.email, 'imagePrefixes': user.image_prefixes}


@bottle.get('/<version:re:[^/]*>/users')
@USERS.auth_api_key(True)  # TODO: Make admin decorator
@check_version
def users(_auth_user):
    if _auth_user.email != 'bwhite@dappervision.com':  # Only me for now
        bottle.abort(401)
    bottle.response.headers["Content-type"] = "application/json"
    return json.dumps([_user_to_dict(USERS.get_user(u)) for u in USERS.list_users()])


@bottle.get('/<version:re:[^/]*>/users/<user:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def user_row(_auth_user, user):
    if _auth_user.email != user:
        bottle.abort(401)
    bottle.response.headers["Content-type"] = "application/json"
    return _user_to_dict(_auth_user)


@bottle.route('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>', 'PATCH')
@bottle.post('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@bottle.delete('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@bottle.get('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_row(_auth_user, table, row):
    with thrift_lock() as thrift:
        manager = PicarusManager(thrift=thrift)
        row = base64.urlsafe_b64decode(row)
        method = bottle.request.method.upper()
        # TODO Check authentication per table
        if not (table and row):
            bottle.abort(400)
        if table not in ('images'):
            bottle.abort(400)
        if method == 'GET':
            verify_row_permissions(_auth_user.image_prefixes, 'r', row)
            columns = sorted(map(base64.urlsafe_b64decode, sorted(bottle.request.params.getall('column'))))
            if columns:
                result = thrift.getRowWithColumns(table, row, columns)
            else:
                result = thrift.getRow(table, row)
            if not result:
                bottle.abort(404)
            return {base64.urlsafe_b64encode(x): base64.b64encode(y.value)
                    for x, y in result[0].columns.items()}
        elif method == 'PATCH':
            verify_row_permissions(_auth_user.image_prefixes, 'w', row)
            mutations = []
            for x in bottle.request.files:
                thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=bottle.request.files[x].file.read())])
            for x in set(bottle.request.params) - set(bottle.request.files):
                print(base64.urlsafe_b64encode(row))
                print(len(bottle.request.params[x]))
                v = base64.b64decode(bottle.request.params[x])
                print(repr(v[:10]))
                mutations.append(hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=v))
            if mutations:
                thrift.mutateRow(table, row, mutations)
            return {}
        elif method == 'POST':
            action = bottle.request.params['action']
            image_column = base64.urlsafe_b64decode(bottle.request.params['imageColumn'])
            results = thrift.get(table, row, image_column)
            if not results:
                print((table, row, image_column))
                bottle.abort(404)
            if action == 'i/classify':
                verify_row_permissions(_auth_user.image_prefixes, 'r', row)
                classifier = _classifier_from_key(manager, base64.urlsafe_b64decode(bottle.request.params['model']))
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps(classifier(results[0].value))
            elif action == 'i/search':
                verify_row_permissions(_auth_user.image_prefixes, 'r', row)
                index = _index_from_key(manager, base64.urlsafe_b64decode(bottle.request.params['model']))
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps(index(results[0].value))
            else:
                bottle.abort(400)
        elif method == 'DELETE':
            verify_row_permissions(_auth_user.image_prefixes, 'w', row)
            thrift.deleteAllRow(table, row)
            return {}
        else:
            bottle.abort(400)


@bottle.delete('/<version:re:[^/]*>/data/<table:re:[^/]+>/<row:re:[^/]+>/<col:re:[^/]+>')
@USERS.auth_api_key(True)
@check_version
def data_row_col(_auth_user, table, row, col):
    with thrift_lock() as thrift:
        row = base64.urlsafe_b64decode(row)
        verify_row_permissions(_auth_user.image_prefixes, 'w', row)
        col = base64.urlsafe_b64decode(col)
        if table not in ('images'):
            bottle.abort(400)
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
        columns = sorted(map(base64.urlsafe_b64decode, sorted(bottle.request.params.getall('column'))))
        # TODO Check authentication per table
        if table not in ('images',):
            raise ValueError('Only images allowed for now!')
        if method == 'GET':
            verify_slice_permissions(_auth_user.image_prefixes, 'r', start_row, stop_row)
            # TODO: Need to verify limits on this scan and check auth
            max_rows = min(100, int(bottle.request.params.get('maxRows', 1)))
            filter_string = bottle.request.params.get('filter')
            print('filter string[%s]' % filter_string)
            exclude_start = bool(int(bottle.request.params.get('excludeStart', 0)))
            cursor = bottle.request.params.get('cacheKey', '')
            # TODO: Allow user to specify cursor, then we can output just the rows
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
            verify_slice_permissions(_auth_user.image_prefixes, 'w', start_row, stop_row)
            # NOTE: This only fetches rows that have a column in meta: (it is a significant optimization)
            # NOTE: Only parameters allowed, no "files" due to memory restrictions
            mutations = []
            for x in bottle.request.params:
                mutations.append(hadoopy_hbase.Mutation(column=base64.urlsafe_b64decode(x), value=bottle.request.params[x]))
            if mutations:
                for row, _ in hadoopy_hbase.scanner(thrift, 'images', start_row=start_row, stop_row=stop_row, filter='KeyOnlyFilter()', columns=['meta:']):
                    print(repr(row))
                    thrift.mutateRow(table, row, mutations)
            return {}
        elif method == 'POST':
            action = bottle.request.params['action']
            if action == 'io/thumbnail':
                verify_slice_permissions(_auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running thumb')
                manager.image_thumbnail(start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/exif':
                verify_slice_permissions(_auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running exif')
                manager.image_exif(start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/preprocess':
                verify_slice_permissions(_auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running preprocessor')
                manager.image_preprocessor(base64.urlsafe_b64decode(bottle.request.params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/classify':
                verify_slice_permissions(_auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running classifier')
                manager.feature_to_prediction(base64.urlsafe_b64decode(bottle.request.params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/feature':
                verify_slice_permissions(_auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running feature')
                manager.image_to_feature(base64.urlsafe_b64decode(bottle.request.params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'io/hash':
                verify_slice_permissions(_auth_user.image_prefixes, 'rw', start_row, stop_row)
                print('Running hash')
                manager.feature_to_hash(base64.urlsafe_b64decode(bottle.request.params['model']), start_row=start_row, stop_row=stop_row)
                return {}
            elif action == 'i/dedupe/identical':
                col = base64.urlsafe_b64decode(bottle.request.params['column'])
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
                verify_slice_permissions(_auth_user.image_prefixes, 'w', start_row, stop_row)
                # Only slices where the start_row can be used as a prefix may be used
                assert start_row and ord(start_row[-1]) != 255 and start_row[:-1] + chr(ord(start_row[-1]) + 1) == stop_row
                print('Running flickr')
                p = {}
                row_prefix = start_row
                assert row_prefix.find(':') != -1
                class_name = bottle.request.params['className']
                query = bottle.request.params.get('query')
                query = class_name if query is None else query
                p['api_key'] = bottle.request.params.get('apiKey', FLICKR_API_KEY)
                p['api_secret'] = bottle.request.params.get('apiSecret', FLICKR_API_SECRET)
                if 'hasGeo' in bottle.request.params:
                    p['has_geo'] = bottle.request.params['hasGeo'] == '1'
                try:
                    p['min_upload_date'] = int(bottle.request.params['minUploadDate'])
                except KeyError:
                    pass
                try:
                    p['max_upload_date'] = int(bottle.request.params['maxUploadDate'])
                except KeyError:
                    pass
                try:
                    p['page'] = int(bottle.request.params['page'])
                except KeyError:
                    pass
                return {'data': {'numRows': crawlers.flickr_crawl(crawlers.HBaseCrawlerStore(thrift, row_prefix), class_name, query, **p)}}
            elif action in ('io/annotate/image/query', 'io/annotate/image/entity', 'io/annotate/image/query_batch'):
                global MTURK_SERVER
                if MTURK_SERVER is not None:
                    bottle.abort(500)  # Need to garbage collect these
                secret = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]
                p = {}
                image_column = base64.urlsafe_b64decode(bottle.request.params['imageColumn'])
                if action == 'io/annotate/image/entity':
                    entity_column = base64.urlsafe_b64decode(bottle.request.params['entityColumn'])
                    p['data'] = 'hbase://localhost:9090/images/%s/%s?entity=%s&image=%s' % (start_row, stop_row, entity_column, image_column)
                    p['type'] = 'image_entity'
                elif action == 'io/annotate/image/query':
                    query = bottle.request.params['query']
                    p['data'] = 'hbase://localhost:9090/images/%s/%s?image=%s' % (start_row, stop_row, image_column)
                    p['type'] = 'image_query'
                    p['query'] = query
                elif action == 'io/annotate/image/query_batch':
                    query = bottle.request.params['query']
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
                        print(repr(row))
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
                            print(cols.keys())
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
                    return _create_model_from_params(manager, path, classifier_sklearn)
                elif path == 'classifier/nbnnlocal':
                    return _create_model_from_params(manager, path, classifier_class_distance_list)
                elif path == 'hasher/rrmedian':
                    return _create_model_from_params(manager, path, hasher_train)
                elif path == 'index/linear':
                    return _create_model_from_params(manager, path, index_train)
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


@bottle.route('/<version:re:[^/]*>/models/<row:re:[^/]+>', 'PATCH')
@bottle.put('/<version:re:[^/]*>/models/<row:re:[^/]+>')
@USERS.auth_api_key()
@check_version
def models_update(row):
    with thrift_lock() as thrift:
        data = bottle.request.json
        kvs = {}
        print(data)
        try:
            kvs['data:notes'] = data['notes']
        except KeyError:
            pass
        try:
            kvs['data:tags'] = data['tags']
        except KeyError:
            pass
        thrift.mutateRow('picarus_models', base64.urlsafe_b64decode(row), [hadoopy_hbase.Mutation(column=k, value=v) for k, v in kvs.items()])
    return {}


@bottle.delete('/<version:re:[^/]*>/models/<row:re:[^/]+>')
@USERS.auth_api_key()
@check_version
def model_delete(row):
    # TODO: Permissions checking
    with thrift_lock() as thrift:
        thrift.deleteAllRow('picarus_models', base64.urlsafe_b64decode(row))
    return {}


# [name]: {module, params}  where params is dict with "name" as key with value {'required': bool, type: (int or float), min, max} with [min, max) or {'required': bool, type: 'bool'} or {'required': enum, vals: [val0, val1, ...]}
PARAM_SCHEMAS = []
PARAM_SCHEMAS.append({'name': 'preprocessor',
                      'type': 'preprocessor',
                      'module': 'imfeat.ImagePreprocessor',
                      'data': 'none',   # none, row, slice
                      'inputs': ['raw_image'],  # abstract columns to be used for input
                      'modelParams': {},
                      'moduleParams': {'compression': {'type': 'enum', 'values': ['jpg']},
                                       'size': {'type': 'int', 'min': 32, 'max': 1025},
                                       'method': {'type': 'enum', 'values': ['force_max_side', 'max_side', 'force_square']}}})

PARAM_SCHEMAS.append({'name': 'histogram',
                      'type': 'feature',
                      'data': 'none',
                      'inputs': ['processed_image'],
                      'module': 'imfeat.Histogram',
                      'modelParams': {'feature_type': {'type': 'const', 'value': 'feature'}},
                      'moduleParams': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                           'hsv', 'luv', 'hls', 'lab', 'gray']},
                                       'num_bins': {'type': 'int', 'min': 1, 'max': 17},
                                       'style': {'type': 'enum', 'values': ['joint', 'planar']}}})

PARAM_SCHEMAS.append({'name': 'svmlinear',
                      'type': 'classifier',
                      'data': 'slice',
                      'inputs': ['feature', 'meta'],
                      'module': 'sklearn.svm.LinearSVC',
                      'modelParams': {'class_positive': {'type': 'str'}, 'classifier_type': {'type': 'const', 'value': 'sklearn_decision_func'}},
                      'moduleParams': {}})

PARAM_SCHEMAS.append({'name': 'rrmedian',
                      'type': 'hasher',
                      'data': 'slice',
                      'inputs': ['feature'],
                      'module': 'image_search.RRMedianHasher',
                      'modelParams': {},
                      'moduleParams': {'hash_bits': {'type': 'int', 'min': 1, 'max': 513}, 'normalize_features': {'type': 'const', 'value': False}}})


PARAM_SCHEMAS.append({'name': 'linear',
                      'type': 'index',
                      'data': 'slice',
                      'inputs': ['hash', 'meta'],
                      'module': 'image_search.LinearHashDB',
                      'modelParams': {},
                      'moduleParams': {}})


PARAM_SCHEMAS.append({'name': 'imageblocks',
                      'type': 'multi_feature',
                      'data': 'none',
                      'inputs': ['processed_image'],
                      'module': 'picarus.modules.ImageBlocks',
                      'modelParams': {'feature_type': {'type': 'const', 'value': 'multi_feature'}},
                      'moduleParams': {'mode': {'type': 'enum', 'values': ['bgr', 'rgb', 'xyz', 'ycrcb',
                                                                           'hsv', 'luv', 'hls', 'lab', 'gray']},
                                       'num_sizes': {'type': 'int', 'min': 1, 'max': 5},
                                       'sbin': {'type': 'int', 'min': 8, 'max': 257}}})

PARAM_SCHEMAS.append({'name': 'nbnnlocal',
                      'type': 'classifier',
                      'data': 'slice',
                      'inputs': ['multi_feature', 'meta'],
                      'module': 'picarus.modules.LocalNBNNClassifier',
                      'modelParams': {'classifier_type': {'type': 'const', 'value': 'class_distance_list'}},
                      'moduleParams': {}})


for x in PARAM_SCHEMAS:
    x['path'] = '/'.join([x['type'], x['name']])

PARAM_SCHEMAS_SERVE = {}
for schema in PARAM_SCHEMAS:
    PARAM_SCHEMAS_SERVE[schema['path']] = dict(schema)


# TODO: Replace this, it is temporary
@bottle.get('/<version:re:[^/]*>/params')
@USERS.auth_api_key()
@check_version
def features():
    bottle.response.headers["Content-type"] = "application/json"
    return json.dumps(PARAM_SCHEMAS)


def _parse_params(schema, prefix):
    kw = {}
    params = schema[prefix + 'Params']
    get_param = lambda x: bottle.request.params[prefix + '-' + x]
    print(params)
    for param_name, param in params.items():
        print((param_name, param))
        if param['type'] == 'enum':
            param_value = get_param(param_name)
            if param_value not in param['values']:
                print(3)
                bottle.abort(400)
            kw[param_name] = param_value
        elif param['type'] == 'int':
            param_value = int(get_param(param_name))
            if not (param['min'] <= param_value < param['max']):
                print(2)
                bottle.abort(400)
            kw[param_name] = param_value
        elif param['type'] == 'const':
            kw[param_name] = param['value']
        elif param['type'] == 'str':
            kw[param_name] = get_param(param_name)
        else:
            print(1)
            bottle.abort(400)
    return kw


def _create_model_from_params(manager, path, create_model):
    try:
        schema = PARAM_SCHEMAS_SERVE[path]
        model_params = _parse_params(schema, 'model')
        module_params = _parse_params(schema, 'module')
        print(model_params)
        print(module_params)
        model_dict = {'name': schema['module'], 'kw': module_params}
        get_key = lambda x: base64.urlsafe_b64decode(bottle.request.params['key-' + x])   # TODO: Verify that model keys exist
        prefix = {'feature': 'feat:', 'preprocessor': 'data:', 'classifier': 'pred:', 'hasher': 'hash:', 'index': 'srch:', 'multi_feature': 'mfeat:'}[schema['type']]
        inputs = {x: get_key(x) for x in schema['inputs']}
        model = create_model(model_dict, model_params, inputs)
        row = manager.input_model_param_to_key(prefix, input=inputs, model=model, name=manager.model_to_name(model_dict), param=model_params)
        return {'row': base64.urlsafe_b64encode(row)}
    except ValueError:
        print(0)
        bottle.abort(400)


@bottle.post('/<version:re:[^/]*>/models/<path:re:.*>')
@USERS.auth_api_key()
@check_version
def models_create(path):
    print_request()
    try:
        #model = call_import(model_dict)
        with thrift_lock() as thrift:
            manager = PicarusManager(thrift=thrift)
            return _create_model_from_params(manager, path, lambda model_dict, model_params, inputs: model_dict)
    except KeyError:
        bottle.abort(400)


@bottle.get('/<version:re:[^/]*>/models')
@USERS.auth_api_key()
@check_version
def models():
    out = []
    prefix_to_name = {'feat:': 'feature',
                      'mfeat:': 'multi_feature',
                      'mask:': 'mask_feature',
                      'pred:': 'classifier',
                      'srch:': 'index',
                      'hash:': 'hasher',
                      'data:': 'preprocessor'}
    with thrift_lock() as thrift:
        for row, cols in hadoopy_hbase.scanner(thrift, 'picarus_models', columns=['data:input', 'data:versions', 'data:prefix', 'data:creation_time', 'data:param', 'data:notes', 'data:name', 'data:tags']):
            name = prefix_to_name[cols['data:prefix']]
            out.append({'inputs': json.loads(cols['data:input']),
                        'versions': json.loads(cols['data:versions']),
                        'param': json.loads(cols['data:param']),
                        'creationTime': float(cols['data:creation_time']),
                        'prefix_pretty': name,
                        'notes': cols['data:notes'],
                        'name': cols['data:name'],
                        'tags': cols['data:tags'],
                        'prefix': cols['data:prefix'],
                        'row': base64.urlsafe_b64encode(row)})
    bottle.response.headers["Content-type"] = "application/json"
    return json.dumps(out)


@bottle.get('/static/<name:re:[^/]+>')
def static(name):
    return bottle.static_file(name, root=os.path.join(os.getcwd(), 'static'))


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
    try:
        email = YUBIKEY.verify(bottle.request.params['otp'])
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
