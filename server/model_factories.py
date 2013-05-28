import msgpack
import numpy as np
import scipy.cluster.vq
import scipy as sp
import random
import picarus_takeout
import kernels


def classifier_sklearn(row_cols, params):
    print('In SKLearn')
    label_features = {0: [], 1: []}
    for row, columns in row_cols:
        label = int(columns['meta'] == params['class_positive'])
        label_features[label].append(columns['feature'])
    labels = [0] * len(label_features[0]) + [1] * len(label_features[1])
    features = label_features[0] + label_features[1]
    features = np.asfarray([msgpack.loads(x)[0] for x in features])
    import sklearn.svm
    classifier = sklearn.svm.LinearSVC()
    classifier.fit(features, np.asarray(labels))
    model_link = {'name': 'picarus.LinearClassifier', 'kw': {'coefficients': classifier.coef_.tolist()[0],
                                                             'intercept': classifier.intercept_[0]}}
    return 'feature', 'binary_class_confidence', model_link


def classifier_kernel_sklearn(row_cols, params):
    label_features = {0: [], 1: []}
    for row, columns in row_cols:
        label = int(columns['meta'] == params['class_positive'])
        label_features[label].append(columns['feature'])
    kernel = {'hik': kernels.histogram_intersection}[params['kernel']]
    labels = [0] * len(label_features[0]) + [1] * len(label_features[1])
    features = label_features[0] + label_features[1]
    features = np.asfarray([msgpack.loads(x)[0] for x in features])
    gram = kernel(features, features)
    import sklearn.svm
    classifier = sklearn.svm.SVC(kernel='precomputed')
    classifier.fit(gram, np.asarray(labels))
    support_vectors = features[classifier.support_, :].ravel().tolist()
    dual_coef = classifier.dual_coef_.ravel().tolist()
    intercept = float(classifier.intercept_.ravel()[0])
    model_link = {'name': 'picarus.KernelClassifier', 'kw': {'support_vectors': support_vectors,
                                                             'dual_coef': dual_coef,
                                                             'intercept': intercept,
                                                             'kernel': params['kernel']}}
    return 'feature', 'binary_class_confidence', model_link


def classifier_localnbnn(row_cols, params):
    features = []
    indeces = []
    num_features = 0
    feature_size = 0
    labels_dict = {}
    labels = []
    for row, columns in row_cols:
        label = columns['meta']
        f, s = msgpack.loads(columns['multi_feature'])
        if label not in labels_dict:
            labels_dict[label] = len(labels_dict)
            labels.append(label)
        feature_size = s[1]
        num_features += s[0]
        features += f
        indeces += [labels_dict[label]] * s[0]
    model_link = {'name': 'picarus.LocalNBNNClassifier', 'kw': {'features': features, 'indeces': indeces, 'labels': labels,
                                                                'feature_size': feature_size, 'max_results': params['max_results']}}
    return 'multi_feature', 'multi_class_distance', model_link


def feature_bovw_mask(row_cols, params):
    features = []
    for row, columns in row_cols:
        cur_feature = msgpack.loads(columns['mask_feature'])
        cur_feature = np.array(cur_feature[0]).reshape((-1, cur_feature[1][2]))
        features += random.sample(cur_feature, min(len(cur_feature), params['max_per_row']))
    features = np.asfarray(features)
    clusters = sp.cluster.vq.kmeans(features, params['num_clusters'])[0]
    num_clusters = clusters.shape[0]
    model_link = {'name': 'picarus.BOVWImageFeature', 'kw': {'clusters': clusters.ravel().tolist(), 'num_clusters': num_clusters,
                                                             'levels': params['levels']}}
    return 'mask_feature', 'feature', model_link


def hasher_spherical(row_cols, params):
    features = []
    for row, columns in row_cols:
        cur_feature = msgpack.loads(columns['feature'])
        features.append(np.array(cur_feature[0]))
    features = np.asfarray(features)
    out = picarus_takeout.spherical_hasher_train(features, params['num_pivots'], params['eps_m'], params['eps_s'], params['max_iters'])
    out = {'pivots': out['pivots'].ravel().tolist(),
           'threshs': out['threshs'].tolist()}
    model_link = {'name': 'picarus.SphericalHasher', 'kw': out}
    return 'feature', 'hash', model_link


def index_spherical(row_cols, params):
    hashes = []
    labels = []
    for row, columns in row_cols:
        hashes.append(columns['hash'])
        labels.append(row)
    hashes = ''.join(hashes)
    model_link = {'name': 'picarus.SphericalHashIndex', 'kw': {'hashes': hashes,
                                                               'indeces': range(len(labels)), 'labels': labels,
                                                               'max_results': params['max_results']}}
    return 'hash', 'distance_image_rows', model_link


def index_hamming_feature2d(row_cols, params):
    hashes = []
    labels = []
    indeces = []
    for row, columns in row_cols:
        f = msgpack.loads(columns['feature2d_binary'])
        hashes.append(f[0])
        indeces += [len(labels)] * f[2][0]
        labels.append(row)
    hashes = ''.join(hashes)
    model_link = {'name': 'picarus.HammingFeature2dHashIndex', 'kw': {'hashes': hashes,
                                                                      'indeces': indeces, 'labels': labels,
                                                                      'max_results': params['max_results'],
                                                                      'max_keypoint_results': params['max_keypoint_results'],
                                                                      'hamming_thresh': params['hamming_thresh']}}
    yield 'feature2d_binary', 'distance_image_rows', model_link


FACTORIES = {'factory/classifier/svmlinear': classifier_sklearn,
             'factory/classifier/svmkernel': classifier_kernel_sklearn,
             'factory/classifier/localnbnn': classifier_localnbnn,
             'factory/feature/bovw': feature_bovw_mask,
             'factory/hasher/spherical': hasher_spherical,
             'factory/index/spherical': index_spherical,
             'factory/index/hamming_feature_2d': index_hamming_feature2d}
