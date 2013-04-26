import base64
import hadoopy_hbase
import msgpack
import numpy as np
import json
import scipy.cluster.vq
import scipy as sp
import random
import picarus_takeout
import kernels
import tables
import os
from driver import PicarusManager


def _setup(start_stop_rows, inputs):
    thrift = hadoopy_hbase.connect()  # TODO: Need to pass in thrift server/port
    manager = PicarusManager(thrift=thrift)
    slices = [base64.b64encode(start_row) + ',' + base64.b64encode(stop_row)
              for start_row, stop_row in start_stop_rows]
    os.nice(5)  # These are background tasks, don't let the CPU get too crazy
    return thrift, manager, slices, {k: base64.b64encode(v) for k, v in inputs.items()}


def classifier_sklearn(queue, params, inputs, schema, start_stop_rows, table, owner):
    thrift, manager, slices, inputsb64 = _setup(start_stop_rows, inputs)
    label_features = {0: [], 1: []}
    for start_row, stop_row in start_stop_rows:
        row_cols = hadoopy_hbase.scanner(thrift, table,
                                         columns=[inputs['feature'], inputs['meta']],
                                         start_row=start_row, stop_row=stop_row)
        for row, cols in row_cols:
            try:
                label = int(cols[inputs['meta']] == params['class_positive'])
                label_features[label].append(cols[inputs['feature']])
            except KeyError:
                continue
    labels = [0] * len(label_features[0]) + [1] * len(label_features[1])
    features = label_features[0] + label_features[1]
    features = np.asfarray([msgpack.loads(x)[0] for x in features])
    import sklearn.svm
    classifier = sklearn.svm.LinearSVC()
    classifier.fit(features, np.asarray(labels))
    factory_info = {'slices': slices, 'num_rows': len(features), 'data': 'slices', 'params': params, 'inputs': inputsb64}
    model_link = {'name': 'picarus.LinearClassifier', 'kw': {'coefficients': classifier.coef_.tolist()[0],
                                                             'intercept': classifier.intercept_[0]}}
    model_chain = tables._takeout_model_chain_from_key(manager, inputs['feature']) + [model_link]
    queue.put(manager.input_model_param_to_key(**{'input': inputs['feature'], 'model_link': model_link, 'model_chain': model_chain, 'input_type': 'feature',
                                                  'output_type': 'binary_class_confidence', 'email': owner, 'name': manager.model_to_name(model_link),
                                                  'factory_info': json.dumps(factory_info)}))


def classifier_kernel_sklearn(queue, params, inputs, schema, start_stop_rows, table, owner):
    thrift, manager, slices, inputsb64 = _setup(start_stop_rows, inputs)
    label_features = {0: [], 1: []}
    for start_row, stop_row in start_stop_rows:
        row_cols = hadoopy_hbase.scanner(thrift, table,
                                         columns=[inputs['feature'], inputs['meta']],
                                         start_row=start_row, stop_row=stop_row)
        for row, cols in row_cols:
            try:
                label = int(cols[inputs['meta']] == params['class_positive'])
                label_features[label].append(cols[inputs['feature']])
            except KeyError:
                continue

    kernel = {'hik': kernels.histogram_intersection}[params['kernel']]
    labels = [0] * len(label_features[0]) + [1] * len(label_features[1])
    features = label_features[0] + label_features[1]
    features = np.asfarray([msgpack.loads(x)[0] for x in features])
    gram = kernel(features, features)
    import sklearn.svm
    classifier = sklearn.svm.SVC(kernel='precomputed')
    classifier.fit(gram, np.asarray(labels))
    factory_info = {'slices': slices, 'num_rows': len(features), 'data': 'slices', 'params': params, 'inputs': inputsb64}
    support_vectors = features[classifier.support_, :].ravel().tolist()
    dual_coef = classifier.dual_coef_.ravel().tolist()
    intercept = float(classifier.intercept_.ravel()[0])
    model_link = {'name': 'picarus.KernelClassifier', 'kw': {'support_vectors': support_vectors,
                                                             'dual_coef': dual_coef,
                                                             'intercept': intercept,
                                                             'kernel': params['kernel']}}
    model_chain = tables._takeout_model_chain_from_key(manager, inputs['feature']) + [model_link]
    queue.put(manager.input_model_param_to_key(**{'input': inputs['feature'], 'model_link': model_link, 'model_chain': model_chain, 'input_type': 'feature',
                                                  'output_type': 'binary_class_confidence', 'email': owner, 'name': manager.model_to_name(model_link),
                                                  'factory_info': json.dumps(factory_info)}))


def classifier_localnbnn(queue, params, inputs, schema, start_stop_rows, table, owner):
    thrift, manager, slices, inputsb64 = _setup(start_stop_rows, inputs)
    features = []
    indeces = []
    num_features = 0
    feature_size = 0
    labels_dict = {}
    labels = []
    for start_row, stop_row in start_stop_rows:
        row_cols = hadoopy_hbase.scanner(thrift, table,
                                         columns=[inputs['multi_feature'], inputs['meta']], start_row=start_row, stop_row=stop_row)
        for _, cols in row_cols:
            try:
                label = cols[inputs['meta']]
                f, s = msgpack.loads(cols[inputs['multi_feature']])
                if label not in labels_dict:
                    labels_dict[label] = len(labels_dict)
                    labels.append(label)
                feature_size = s[1]
                num_features += s[0]
                features += f
                indeces += [labels_dict[label]] * s[0]
            except KeyError:
                pass
    factory_info = {'slices': slices, 'data': 'slices', 'params': params, 'inputs': inputsb64}
    model_link = {'name': 'picarus.LocalNBNNClassifier', 'kw': {'features': features, 'indeces': indeces, 'labels': labels,
                                                                'feature_size': feature_size, 'max_results': params['max_results']}}
    model_chain = tables._takeout_model_chain_from_key(manager, inputs['multi_feature']) + [model_link]
    queue.put(manager.input_model_param_to_key(**{'input': inputs['multi_feature'], 'model_link': model_link, 'model_chain': model_chain,
                                                  'input_type': 'multi_feature', 'output_type': 'multi_class_distance',
                                                  'email': owner, 'name': manager.model_to_name(model_link), 'factory_info': json.dumps(factory_info)}))


def feature_bovw_mask(queue, params, inputs, schema, start_stop_rows, table, owner):
    thrift, manager, slices, inputsb64 = _setup(start_stop_rows, inputs)
    features = []
    for start_row, stop_row in start_stop_rows:
        row_cols = hadoopy_hbase.scanner(thrift, table,
                                         columns=[inputs['mask_feature']],
                                         start_row=start_row, stop_row=stop_row)
        for row, cols in row_cols:
            cur_feature = msgpack.loads(cols[inputs['mask_feature']])
            cur_feature = np.array(cur_feature[0]).reshape((-1, cur_feature[1][2]))
            features += random.sample(cur_feature, min(len(cur_feature), params['max_per_row']))
            print(len(features))
    features = np.asfarray(features)
    clusters = sp.cluster.vq.kmeans(features, params['num_clusters'])[0]
    num_clusters = clusters.shape[0]
    factory_info = {'slices': slices, 'num_features': len(features), 'data': 'slices', 'params': params, 'inputs': inputsb64}
    model_link = {'name': 'picarus.BOVWImageFeature', 'kw': {'clusters': clusters.ravel().tolist(), 'num_clusters': num_clusters,
                                                             'levels': params['levels']}}
    model_chain = tables._takeout_model_chain_from_key(manager, inputs['mask_feature']) + [model_link]
    queue.put(manager.input_model_param_to_key(**{'input': inputs['mask_feature'], 'model_link': model_link, 'model_chain': model_chain, 'input_type': 'feature',
                                                  'output_type': 'feature', 'email': owner, 'name': manager.model_to_name(model_link),
                                                  'factory_info': json.dumps(factory_info)}))


def hasher_spherical(queue, params, inputs, schema, start_stop_rows, table, owner):
    thrift, manager, slices, inputsb64 = _setup(start_stop_rows, inputs)
    features = []
    for start_row, stop_row in start_stop_rows:
        row_cols = hadoopy_hbase.scanner(thrift, table,
                                         columns=[inputs['feature']],
                                         start_row=start_row, stop_row=stop_row)
        for row, cols in row_cols:
            cur_feature = msgpack.loads(cols[inputs['feature']])
            features.append(np.array(cur_feature[0]))
    print('num_features[%d]' % len(features))
    features = np.asfarray(features)
    out = picarus_takeout.spherical_hasher_train(features, params['num_pivots'], params['eps_m'], params['eps_s'], params['max_iters'])
    out = {'pivots': out['pivots'].ravel().tolist(),
           'threshs': out['threshs'].tolist()}
    #out = picarus.modules.spherical_hash.train_takeout(features, params['num_pivots'], params['eps_m'], params['eps_s'], params['max_iters'])
    factory_info = {'slices': slices, 'num_features': len(features), 'data': 'slices', 'params': params, 'inputs': inputsb64}
    model_link = {'name': 'picarus.SphericalHasher', 'kw': out}
    model_chain = tables._takeout_model_chain_from_key(manager, inputs['feature']) + [model_link]
    queue.put(manager.input_model_param_to_key(**{'input': inputs['feature'], 'model_link': model_link, 'model_chain': model_chain, 'input_type': 'feature',
                                                  'output_type': 'hash', 'email': owner, 'name': manager.model_to_name(model_link),
                                                  'factory_info': json.dumps(factory_info)}))


def index_spherical(queue, params, inputs, schema, start_stop_rows, table, owner):
    thrift, manager, slices, inputsb64 = _setup(start_stop_rows, inputs)
    hashes = []
    labels = []
    for start_row, stop_row in start_stop_rows:
        row_cols = hadoopy_hbase.scanner(thrift, table,
                                         columns=[inputs['hash']],
                                         start_row=start_row, stop_row=stop_row)
        for row, cols in row_cols:
            hashes.append(cols[inputs['hash']])
            labels.append(row)
    hashes = ''.join(hashes)
    factory_info = {'slices': slices, 'num_hashes': len(labels), 'data': 'slices', 'params': params, 'inputs': inputsb64}
    model_link = {'name': 'picarus.SphericalHashIndex', 'kw': {'hashes': hashes,
                                                               'indeces': range(len(labels)), 'labels': labels,
                                                               'max_results': params['max_results']}}
    model_chain = tables._takeout_model_chain_from_key(manager, inputs['hash']) + [model_link]
    queue.put(manager.input_model_param_to_key(**{'input': inputs['hash'], 'model_link': model_link, 'model_chain': model_chain, 'input_type': 'hash',
                                                  'output_type': 'distance_image_rows', 'email': owner, 'name': manager.model_to_name(model_link),
                                                  'factory_info': json.dumps(factory_info)}))


def index_hamming_feature2d(queue, params, inputs, schema, start_stop_rows, table, owner):
    thrift, manager, slices, inputsb64 = _setup(start_stop_rows, inputs)
    hashes = []
    #keypoints = []
    labels = []
    indeces = []
    for start_row, stop_row in start_stop_rows:
        row_cols = hadoopy_hbase.scanner(thrift, table,
                                         columns=[inputs['feature2d_binary']],
                                         start_row=start_row, stop_row=stop_row)
        for row, cols in row_cols:
            f = msgpack.loads(cols[inputs['feature2d_binary']])
            print(f[2][0])
            hashes.append(f[0])
            #keypoints += f[1]
            indeces += [len(labels)] * f[2][0]
            labels.append(row)
            print(len(labels))
    hashes = ''.join(hashes)
    factory_info = {'slices': slices, 'num_hashes': len(indeces), 'num_images': len(labels), 'data': 'slices', 'params': params, 'inputs': inputsb64}
    #'keypoints': keypoints,
    model_link = {'name': 'picarus.HammingFeature2dHashIndex', 'kw': {'hashes': hashes,
                                                                      'indeces': indeces, 'labels': labels,
                                                                      'max_results': params['max_results'],
                                                                      'max_keypoint_results': params['max_keypoint_results'],
                                                                      'hamming_thresh': params['hamming_thresh']}}
    model_chain = tables._takeout_model_chain_from_key(manager, inputs['feature2d_binary']) + [model_link]
    queue.put(manager.input_model_param_to_key(**{'input': inputs['feature2d_binary'], 'model_link': model_link, 'model_chain': model_chain, 'input_type': 'feature2d_binary',
                                                  'output_type': 'distance_image_rows', 'email': owner, 'name': manager.model_to_name(model_link),
                                                  'factory_info': json.dumps(factory_info)}))


FACTORIES = {'factory/classifier/svmlinear': classifier_sklearn,
             'factory/classifier/svmkernel': classifier_kernel_sklearn,
             'factory/classifier/localnbnn': classifier_localnbnn,
             'factory/feature/bovw': feature_bovw_mask,
             'factory/hasher/spherical': hasher_spherical,
             'factory/index/spherical': index_spherical,
             'factory/index/hamming_feature_2d': index_hamming_feature2d}
