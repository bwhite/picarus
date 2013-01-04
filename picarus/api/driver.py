import hadoopy_hbase
import logging
import time
import tempfile
import zlib
import json
import os
import random
import cPickle as pickle
import picarus.api
import image_search
import itertools
import numpy as np
import base64
import picarus._features
import picarus.modules
import picarus.api
import sklearn.svm
import imfeat
import scipy as sp
import scipy.cluster.vq
import hashlib
import subprocess
from confmat import save_confusion_matrix

logging.basicConfig(level=logging.DEBUG)

output_hdfs = 'picarus_temp/%f/' % time.time()


def hashes_to_index(si, index, metadata, hashes):
    hashes = np.ascontiguousarray(np.asfarray([np.fromstring(h, dtype=np.uint8) for h in hashes]))
    si.metadata.extend(metadata)
    index = index.store_hashes(hashes, np.arange(len(metadata), dtype=np.uint64))
    si.index = pickle.dumps(index, -1)
    si.index_format = si.PICKLE
    return si.SerializeToString()


def features_to_classifier(classifier, labels, features):
    features = np.asfarray([picarus.api.np_fromstring(x) for x in features])
    classifier.fit(features, np.asarray(labels))


def get_version(module_name):
    prev_dir = os.path.abspath('.')
    try:
        module_dir = __import__(module_name).__path__[0]
    except ImportError:
        raise ValueError('Module [%s] could not be imported!' % module_name)
    except AttributeError:
        raise ValueError('Module [%s] directory could not be found!' % module_name)
    try:
        os.chdir(module_dir)
        return subprocess.Popen('git log -1 --pretty=format:%H'.split(), stdout=subprocess.PIPE).communicate()[0]
    finally:
        os.chdir(prev_dir)


class PicarusManager(object):

    def __init__(self, thrift=None):
        self.image_orig_column = 'data:image'
        self.image_column = 'data:image_320'
        self.thumbnails_column = 'data:image_75sq'
        self.images_table = 'images'
        self.models_table = 'picarus_models'
        self.hb = thrift if thrift is not None else hadoopy_hbase.connect()
        self.max_cell_size = 10 * 1024 * 1024  # 10MB
        # Feature Settings
        self.superpixel_column = 'feat:superpixel'
        # Feature Hasher settings
        self.hb = hadoopy_hbase.connect()
        # Feature Classifier settings
        self.feature_classifier_row = self.images_table
        # Mask Hasher settings
        self.texton_num_classes = 8
        self.texton_classes = json.load(open('class_colors.js'))
        # Index Settings
        self.class_column = 'meta:class_2'
        self.indoor_class_column = 'meta:class_0'
        self.num_mappers = 6
        self.versions = self.get_versions()
        self.model_chunks_column = 'data:model_chunks'
        self.model_column = 'data:model'
        self.input_column = 'data:input'
        self.param_column = 'data:param'
        self.versions_column = 'data:versions'
        self.prefix_column = 'data:prefix'
        self.model_type_column = 'data:model_type'
        self.creation_time_column = 'data:creation_time'

    def get_versions(self):
        return {x: get_version(x) for x in ['picarus', 'imfeat', 'imseg', 'hadoopy', 'impoint', 'hadoopy_hbase']}

    def input_model_param_to_key(self, prefix, input, model, param={}):
        assert isinstance(input, dict)
        assert isinstance(param, dict)
        dumps = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':'))
        input = {k: base64.b64encode(v) for k, v in input.items()}
        param = {k: base64.b64encode(v) for k, v in param.items()}
        input_str = dumps(input)
        param_str = dumps(param)
        if isinstance(model, dict):
            model_type = 'json'
            model_str = dumps(model)
        else:
            model_type = 'pickle'
            model_str = dumps(base64.b64encode(zlib.compress(pickle.dumps(model, -1))))
        input_model_param_str = dumps([input_str, model_str, param_str])
        model_key = prefix + hashlib.sha1(input_model_param_str).digest()
        # Only write if the row doesn't exist
        if not self.hb.get(self.models_table, model_key, self.prefix_column):
            cols = [hadoopy_hbase.Mutation(column=self.model_type_column, value=model_type),
                    hadoopy_hbase.Mutation(column=self.input_column, value=input_str),
                    hadoopy_hbase.Mutation(column=self.param_column, value=param_str),
                    hadoopy_hbase.Mutation(column=self.versions_column, value=json.dumps(self.versions)),
                    hadoopy_hbase.Mutation(column=self.prefix_column, value=prefix),
                    hadoopy_hbase.Mutation(column=self.creation_time_column, value=str(time.time()))]
            chunk_count = 0
            while model_str:
                cols.append(hadoopy_hbase.Mutation(column=self.model_column + '-%d' % chunk_count, value=model_str[:self.max_cell_size]))
                model_str = model_str[self.max_cell_size:]
                print(chunk_count)
                chunk_count += 1
            cols.append(hadoopy_hbase.Mutation(column=self.model_chunks_column, value=np.array(chunk_count, dtype=np.uint32).tostring()))
            self.hb.mutateRow(self.models_table, model_key, cols)
        else:
            print('Model exists!')
        return model_key

    def key_to_input_model_param(self, key):
        columns = self.hb.getRowWithColumns(self.models_table, key, [self.input_column, self.model_chunks_column, self.param_column])[0].columns
        input, param = json.loads(columns[self.input_column].value), json.loads(columns[self.param_column].value)
        model_chunks = np.fromstring(columns[self.model_chunks_column].value, dtype=np.uint32)
        columns = self.hb.getRowWithColumns(self.models_table, key, [self.model_column + '-%d' % x for x in range(model_chunks)])[0].columns
        model = ''.join(columns[self.model_column + '-%d' % x].value for x in range(model_chunks))
        model = json.loads(model)
        input = {k: base64.b64decode(v) for k, v in input.items()}
        param = {k: base64.b64decode(v) for k, v in param.items()}
        if not isinstance(model, dict):
            model = pickle.loads(zlib.decompress(base64.b64decode(model)))
        return input, model, param

    def create_tables(self):
        self.hb.createTable(self.models_table, [hadoopy_hbase.ColumnDescriptor('data:')])

    def image_preprocessor(self, model_key, **kw):
        input_dict, model_dict, _ = self.key_to_input_model_param(model_key)
        model_fp = picarus.api.model_tofile(model_dict)
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(model_key),
                   'MODEL_FN': os.path.basename(model_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/image_preprocess.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, files=[model_fp.name], columns=[input_dict['image']], single_value=True,
                             cmdenvs=cmdenvs, dummy_fp=model_fp, **kw)

    def image_to_feature(self, feature_key, **kw):
        input_dict, feature, params = self.key_to_input_model_param(feature_key)
        feature_fp = picarus.api.model_tofile(feature)
        feature_type = params['feature_type']
        assert feature_type in ('feature', 'multi_feature', 'mask_feature')
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(feature_key),
                   'FEATURE_FN': os.path.basename(feature_fp.name),
                   'FEATURE_TYPE': feature_type}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/image_to_feature.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[input_dict['image']], single_value=True,
                             cmdenvs=cmdenvs, files=[feature_fp.name],
                             jobconfs={'mapred.task.timeout': '6000000'}, dummy_fp=feature_fp, **kw)

    def features_to_hasher(self, feature_key, hasher, **kw):
        features = hadoopy_hbase.scanner_column(self.hb, self.images_table, feature_key, **kw)
        hasher = hasher.train(picarus.api.np_fromstring(x) for x in features)
        k = image_retrieval.input_model_param_to_key('hash:', input={'feature': feature_key}, model=hasher)
        print(repr(k))
        return k

    def feature_to_hash(self, model_key, **kw):
        input_dict, hasher, _ = self.key_to_input_model_param(model_key)
        hasher_fp = picarus.api.model_tofile(hasher)
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(model_key),
                   'HASHER_FN': os.path.basename(hasher_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/feature_to_hash.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[input_dict['feature']], files=[hasher_fp.name], single_value=True,
                             cmdenvs=cmdenvs, dummy_fp=hasher_fp, **kw)

    def _classifier_feature(self, cp, feature):
        if isinstance(feature, dict):
            cp.feature = json.dumps(feature)
            cp.feature_format = cp.JSON_IMPORT
        else:
            cp.feature = pickle.dumps(feature, -1)
            cp.feature_format = cp.PICKLE

    def features_to_classifier_class_distance_list(self, feature_key, metadata_column, classifier, **kw):
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[feature_key, metadata_column], **kw)
        label_values = ((cols[metadata_column], np.asfarray(picarus.api.np_fromstring(cols[feature_key]))) for _, cols in row_cols)
        classifier.train(label_values)
        cp = picarus.api.Classifier()
        cp.name = '%s-%s' % (feature_key, metadata_column)
        feature_input, feature, _ = self.key_to_input_model_param(feature_key)
        self._classifier_feature(cp, feature)
        cp.classifier_format = cp.PICKLE
        cp.classifier_type = cp.CLASS_DISTANCE_LIST
        # TODO: Store metadata such as classifier_type
        classifier_ser = pickle.dumps(classifier, -1)
        print(len(classifier_ser))
        k = image_retrieval.input_model_param_to_key('pred:', input={'feature': feature_key, 'meta': metadata_column},
                                                     model=classifier)
        print(repr(k))
        return k

    def features_to_classifier_sklearn_decision_func(self, feature_key, metadata_column, class_positive, classifier, max_per_label=None, **kw):
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[feature_key, metadata_column], **kw)
        label_features = {0: [], 1: []}
        for row, cols in row_cols:
            if max_per_label is not None and len(label_features[0]) >= max_per_label and len(label_features[1]) >= max_per_label:
                break
            label = int(cols[metadata_column] == class_positive)
            if max_per_label is None or len(label_features[label]) < max_per_label:
                label_features[label].append(cols[feature_key])
                print label, cols[metadata_column]
            else:
                print('Skipping[%d]' % label)
        labels = [0] * len(label_features[0]) + [1] * len(label_features[1])
        features = label_features[0] + label_features[1]
        features = np.asfarray([picarus.api.np_fromstring(x) for x in features])
        classifier.fit(features, np.asarray(labels))
        cp = picarus.api.Classifier()
        cp.name = '%s-%s-%s' % (feature_key, metadata_column, class_positive)
        feature_input, feature, _ = self.key_to_input_model_param(feature_key)
        self._classifier_feature(cp, feature)
        cp.classifier = pickle.dumps(classifier, -1)
        cp.classifier_format = cp.PICKLE
        k = image_retrieval.input_model_param_to_key('pred:', input={'feature': feature_key, 'meta': metadata_column},
                                                     model=cp.SerializeToString(), param={'class_positive': class_positive})
        print(repr(k))
        return k

    def feature_to_prediction(self, model_key, **kw):
        input_dict, classifier, _ = self.key_to_input_model_param(model_key)
        classifier_fp = tempfile.NamedTemporaryFile()
        classifier_fp.write(classifier)
        classifier_fp.flush()
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(model_key),
                   'CLASSIFIER_FN': os.path.basename(classifier_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/feature_to_prediction.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[input_dict['feature']], files=[classifier_fp.name], single_value=True,
                             cmdenvs=cmdenvs, dummy_fp=classifier_fp, **kw)

    def hashes_to_index(self, hasher_key, metadata_column, index, **kw):
        si = picarus.api.SearchIndex()
        si.name = hasher_key
        hasher_input, hasher, _ = self.key_to_input_model_param(hasher_key)
        feature_input, feature, _ = self.key_to_input_model_param(hasher_input['feature'])
        si.feature = json.dumps(feature)
        si.hash = pickle.dumps(hasher, -1)
        si.hash_format = si.PICKLE
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[hasher_key, metadata_column], **kw)
        metadata, hashes = zip(*[(json.dumps([cols[metadata_column], base64.b64encode(row)]), cols[hasher_key])
                                 for row, cols in row_cols])
        hashes = np.ascontiguousarray(np.asfarray([np.fromstring(h, dtype=np.uint8) for h in hashes]))
        si.metadata.extend(metadata)
        index = index.store_hashes(hashes, np.arange(len(metadata), dtype=np.uint64))
        si.index = pickle.dumps(index, -1)
        si.index_format = si.PICKLE
        k = image_retrieval.input_model_param_to_key('srch:', input={'hash': hasher_key, 'meta': metadata_column}, model=si.SerializeToString())
        open('feature_index.pb', 'w').write(si.SerializeToString())
        print(repr(k))
        return k

    def _tempfile(self, data, suffix=''):
        fp = tempfile.NamedTemporaryFile(suffix=suffix)
        fp.write(data)
        fp.flush()
        return fp

    def _feature_to_hash(self, hasher, input_table, input_column, output_table, output_column, **kw):
        hasher_fp = picarus.api.model_tofile(hasher)
        cmdenvs = {'HBASE_TABLE': input_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(output_column),
                   'HASHER_FN': os.path.basename(hasher_fp.name)}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'hadoop/feature_to_hash.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[input_column], files=[hasher_fp.name], single_value=True,
                             cmdenvs=cmdenvs, dummy_fp=hasher_fp, **kw)

    def _feature_to_prediction(self, classifier, input_table, input_column, output_table, output_column, **kw):
        classifier_fp = tempfile.NamedTemporaryFile()
        classifier_fp.write(classifier)
        classifier_fp.flush()
        cmdenvs = {'HBASE_TABLE': input_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(output_column),
                   'CLASSIFIER_FN': os.path.basename(classifier_fp.name)}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'hadoop/feature_to_prediction.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[input_column], files=[classifier_fp.name], single_value=True,
                             cmdenvs=cmdenvs, dummy_fp=classifier_fp, **kw)

    def prediction_to_conf_gt(self, **kw):
        self._prediction_to_conf_gt(self.feature_class_positive, self.images_table, self.feature_prediction_column, self.indoor_class_column, **kw)

    def _prediction_to_conf_gt(self, class_positive, input_table, input_prediction_column, input_class_column, **kw):
        row_cols = hadoopy_hbase.scanner(self.hb, input_table,
                                         columns=[input_prediction_column, input_class_column], **kw)
        pos_confs = []
        neg_confs = []
        for row, cols in row_cols:
            pred = float(np.fromstring(cols[input_prediction_column], dtype=np.double)[0])
            print(repr(row))
            if cols[input_class_column] == class_positive:
                pos_confs.append(pred)
            else:
                neg_confs.append(pred)
        pos_confs.sort()
        neg_confs.sort()
        open('confs.js', 'w').write(json.dumps({'pos_confs': pos_confs, 'neg_confs': neg_confs}))
        print(len(pos_confs))
        print(len(neg_confs))

    def _build_index(self, si, index, input_table, input_hash_column, input_class_column, output_table, output_row, output_column, **kw):
        row_dict = hadoopy_hbase.HBaseRowDict(output_table,
                                              output_column, db=self.hb)
        row_cols = hadoopy_hbase.scanner(self.hb, input_table,
                                         columns=[input_hash_column, input_class_column], **kw)
        metadata, hashes = zip(*[(json.dumps([cols[input_class_column], base64.b64encode(row)]), cols[input_hash_column])
                                 for row, cols in row_cols])
        row_dict[output_row] = hashes_to_index(si, index, metadata, hashes)

    def _get_texton(self, classifier_key):
        forests = []
        threshs = [0.]
        # TODO: Have a way to verify that the input columns match for things that use this
        ilp_input, ilp = self.key_to_input_model_param(classifier_key)[:2]
        for x in ['outdoor', 'indoor']:
            tp = pickle.load(open('tree_ser-%s-texton.pkl' % x))
            tp2 = pickle.load(open('tree_ser-%s-integral.pkl' % x))
            forests.append({'tp': tp, 'tp2': tp2})
        return picarus._features.TextonILPPredict(num_classes=self.texton_num_classes, ilp=ilp,
                                                  forests=forests, threshs=threshs)

    def annotation_masks_to_hbase(self):
        import redis
        import ast
        import imfeat
        import cv2
        r = redis.StrictRedis(port=6381, db=6)
        responses = [r.hgetall(x) for x in r.keys()]
        print('Total Responses[%d]' % len(responses))
        image_class_segments = {}  # [row][class_name] = segments
        for x in responses:
            if 'user_data' in x:
                x['user_data'] = ast.literal_eval(x['user_data'])
                if x['user_data']['segments']:
                    row_key = x['image']
                    image_class_segments.setdefault(row_key, {}).setdefault(x['user_data']['name'], []).append(x['user_data']['segments'])
        for row_key, class_segments in image_class_segments.items():
            columns = dict((x, y.value) for x, y in self.hb.getRowWithColumns(self.images_table, row_key, [self.image_column, self.superpixel_column])[0].columns.items())
            image = imfeat.image_fromstring(columns[self.image_column])
            segments = json.loads(columns[self.superpixel_column])
            class_masks = {}
            class_masks = np.zeros((image.shape[0], image.shape[1], self.texton_num_classes))
            for name, user_segment_groups in class_segments.items():
                cur_mask = np.zeros(image.shape[:2], dtype=np.uint8)
                for user_segment_group in user_segment_groups:
                    for user_segment in user_segment_group:
                        hull = segments[user_segment]
                        hull = np.asarray(hull).astype(np.int32).reshape(1, -1, 2)
                        mask_color = 255
                        cv2.drawContours(cur_mask, hull, -1, mask_color, -1)
                        cv2.drawContours(cur_mask, hull, -1, mask_color, 2)
                class_masks[:, :, self.texton_classes[name]['mask_num']] = cur_mask / 255.
            class_masks_ser = picarus.api.np_tostring(class_masks)
            print('Storing row [%s]' % repr(row_key))
            self.hb.mutateRow(self.images_table, row_key, [hadoopy_hbase.Mutation(column=self.masks_gt_column, value=class_masks_ser)])

    def cluster_points_local(self, **kw):
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[self.image_column], **kw)
        feature_func = imfeat.HOGLatent(16)
        num_clusters = 100
        features = []
        for row, columns in row_cols:
            image = imfeat.image_fromstring(columns[self.image_column])
            features.append(feature_func.compute_dense(image))
        features = np.vstack(features)
        clusters = sp.cluster.vq.kmeans(features, num_clusters)[0]
        print(clusters.shape)
        json.dump(clusters.tolist(), open('clusters.js', 'w'))


if __name__ == '__main__':
    image_retrieval = PicarusManager()
    #image_retrieval.create_tables()

    def run_preprocessor(k, **kw):
        image_retrieval.image_preprocessor(k, **kw)

    def create_preprocessor(model):
        k = image_retrieval.input_model_param_to_key('data:', input={'image': 'data:image'}, model=model)
        print(repr(k))
        return k

    def run_feature(k, **kw):
        image_retrieval.image_to_feature(k, **kw)

    def create_feature(image_key, model):
        k = image_retrieval.input_model_param_to_key('feat:', input={'image': image_key}, model=model, param={'feature_type': 'feature'})
        print(repr(k))
        return k

    def create_mask_feature(image_key, model):
        k = image_retrieval.input_model_param_to_key('mask:', input={'image': image_key}, model=model, param={'feature_type': 'mask_feature'})
        print(repr(k))
        return k

    def create_multi_feature(image_key, model):
        k = image_retrieval.input_model_param_to_key('mfeat:', input={'image': image_key}, model=model, param={'feature_type': 'multi_feature'})
        print(repr(k))
        return k

    def run_hasher(k, **kw):
        image_retrieval.feature_to_hash(k, **kw)

    def create_hasher(feature_key, hasher, **kw):
        k = image_retrieval.features_to_hasher(feature_key, hasher, max_rows=10000)
        return k

    def create_index(hasher_key, metadata_column, index, **kw):
        k = image_retrieval.hashes_to_index(hasher_key, metadata_column, index, **kw)
        return k

    def run_classifier(k, **kw):
        image_retrieval.feature_to_prediction(k, **kw)

    def create_classifier_sklearn_decision_func(feature_key, metadata_column, class_positive, classifier, **kw):
        k = image_retrieval.features_to_classifier_sklearn_decision_func(feature_key, metadata_column, class_positive, classifier, max_per_label=5000, **kw)
        return k

    def create_classifier_class_distance_list(feature_key, metadata_column, classifier, **kw):
        k = image_retrieval.features_to_classifier_class_distance_list(feature_key, metadata_column, classifier, **kw)
        return k

    image_key = create_preprocessor({'name': 'imfeat.ImagePreprocessor', 'kw': {'method': 'max_side', 'size': 80, 'compression': 'jpg'}})
    #run_preprocessor(image_key, start_row='logos:good', stop_row='logos:gooe')
    feature_key = create_multi_feature(image_key, {'name': 'picarus.modules.ImageBlocks', 'kw': {'sbin': 16, 'mode': 'lab', 'num_sizes': 3}})
    #run_feature(feature_key, start_row='logos:good', stop_row='logos:gooe')
    create_classifier_class_distance_list(feature_key, 'meta:class', picarus.modules.LocalNBNNClassifier(), start_row='logos:good', stop_row='logos:gooe')

    #feature_key = create_feature(image_key, {'name': 'picarus._features.HOGBoVW', 'kw': {'clusters': json.load(open('clusters.js')), 'levels': 2, 'sbin': 16, 'blocks': 1}})
    #run_feature(feature_key, start_row='sun397:', stop_row='sun398:')
    #hasher_key = create_hasher(feature_key, image_search.RRMedianHasher(hash_bits=256, normalize_features=False), start_row='sun397:train', stop_row='sun397:traio')
    #run_hasher(hasher_key, start_row='sun397:', stop_row='sun398:')
    #create_index(hasher_key, 'meta:class_2', image_search.LinearHashDB(), start_row='sun397:train', stop_row='sun397:traio')
    #classifier_key = create_classifier(feature_key, 'meta:class_0', 'indoor', sklearn.svm.LinearSVC(), start_row='sun397:train', stop_row='sun397:traio')
    #run_classifier(classifier_key, start_row='sun397:', stop_row='sun398:')
    # Masks
    #feature_key = create_mask_feature(image_key, image_retrieval._get_texton(base64.b64decode('cHJlZDqOWGdqIgoVV27QmARQoqxb15Y+9A==')))
    #run_feature(feature_key, start_row='sun397:', stop_row='sun398:')
