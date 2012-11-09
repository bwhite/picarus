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
import picarus.api
import sklearn.svm

logging.basicConfig(level=logging.DEBUG)

output_hdfs = 'picarus_temp/%f/' % time.time()


def features_to_hasher(hasher, features):
    return pickle.dumps(hasher.train(picarus.api.np_fromstring(x) for x in features), -1)


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


class ImageRetrieval(object):

    def __init__(self):
        self.image_orig_column = 'data:image'
        self.image_column = 'data:image_320'
        self.thumbnails_column = 'data:image_75sq'
        self.images_table = 'images'
        self.models_table = 'picarus_models'
        self.hb = hadoopy_hbase.connect()
        # Feature Settings
        self.feature_dict = {'name': 'imfeat.GIST'}
        self.feature_name = 'gist'
        #self.feature_dict = {'name': 'imfeat.PyramidHistogram', 'args': ['lab'], 'kw': {'levels': 3, 'num_bins': [4, 11, 11]}}
        #self.feature_name = 'lab_pyramid_histogram_3level_4_11_11'
        self.feature_column = 'feat:' + self.feature_name
        # Feature Hasher settings
        self.feature_hasher_row = self.images_table
        self.feature_hasher_column = 'data:hasher_' + self.feature_name
        self.hb = hadoopy_hbase.connect()
        self.feature_hash_column = 'hash:' + self.feature_name
        # Feature Classifier settings
        self.feature_classifier_row = self.images_table
        self.feature_classifier_column = 'data:classifier_' + self.feature_name
        self.feature_prediction_column = 'hash:predict_' + self.feature_name
        self.feature_class_positive = 'indoor'
        # Mask Hasher settings
        self.masks_hasher_row = 'masks'
        self.masks_hasher_column = 'data:hasher_masks'
        self.masks_hash_column = 'hash:masks'
        # Index Settings
        self.feature_index_row = self.images_table
        self.feature_index_column = 'data:index_' + self.feature_name
        self.masks_index_row = 'masks'
        self.masks_index_column = 'data:index_masks'
        self.masks_column = 'feat:masks'
        self.class_column = 'meta:class_2'
        self.indoor_class_column = 'meta:class_0'
        self.num_mappers = 2

    def create_tables(self):
        self.hb.createTable(self.models_table, [hadoopy_hbase.ColumnDescriptor('data:')])

    def image_resize(self):
        cmdenvs = {'HBASE_INPUT_COLUMN': self.image_orig_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.image_column,
                   'MAX_SIDE': 320}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'image_resize.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs)

    def image_thumbnail(self):
        cmdenvs = {'HBASE_INPUT_COLUMN': self.image_orig_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.thumbnails_column,
                   'SIZE': 75}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'image_thumbnail.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs)

    def image_to_feature(self):
        self._image_to_feature(self.feature_dict, self.images_table, self.image_column, self.images_table, self.feature_column)

    def image_to_masks(self):
        self._image_to_feature(self._get_texton(), self.images_table, self.image_column, self.images_table, self.masks_column)

    def _image_to_feature(self, feature, input_table, input_column, output_table, output_column):
        feature_fp = picarus.api.model_tofile(feature)
        cmdenvs = {'HBASE_INPUT_COLUMN': input_column,
                   'HBASE_TABLE': output_table,
                   'HBASE_OUTPUT_COLUMN': output_column,
                   'FEATURE_FN': os.path.basename(feature_fp.name)}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'image_to_feature.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs, files=[feature_fp.name],
                             jobconfs={'mapred.task.timeout': '6000000'}, dummy_fp=feature_fp)

    def features_to_hasher(self, **kw):
        hash_bits = 256
        hasher = image_search.RRMedianHasher(hash_bits, normalize_features=False)
        self._features_to_hasher(hasher, self.images_table, self.feature_column, self.models_table, self.feature_hasher_row, self.feature_hasher_column, **kw)

    def masks_to_hasher(self, **kw):
        hash_bits = 8
        hasher = image_search.HIKHasherGreedy(hash_bits=hash_bits)
        self._features_to_hasher(hasher, self.images_table, self.masks_column, self.models_table, self.masks_hasher_row, self.masks_hasher_column, **kw)

    def _features_to_hasher(self, hasher, input_table, input_column, output_table, output_row, output_column, **kw):
        row_dict = hadoopy_hbase.HBaseRowDict(output_table, output_column, db=self.hb)
        features = hadoopy_hbase.scanner_column(self.hb, input_table, input_column, **kw)
        row_dict[output_row] = features_to_hasher(hasher, features)

    def _tempfile(self, data, suffix=''):
        fp = tempfile.NamedTemporaryFile(suffix=suffix)
        fp.write(data)
        fp.flush()
        return fp

    def feature_to_hash(self):
        self._feature_to_hash(self.get_feature_hasher(), self.images_table, self.feature_column, self.images_table, self.feature_hash_column)

    def masks_to_hash(self):
        self._feature_to_hash(self.get_masks_hasher(), self.images_table, self.masks_column, self.images_table, self.masks_hash_column)

    def _feature_to_hash(self, hasher, input_table, input_column, output_table, output_column, **kw):
        hasher_fp = picarus.api.model_tofile(hasher)
        cmdenvs = {'HBASE_INPUT_COLUMN': input_column,
                   'HBASE_TABLE': input_table,
                   'HBASE_OUTPUT_COLUMN': output_column,
                   'HASHER_FN': os.path.basename(hasher_fp.name)}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'feature_to_hash.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[cmdenvs['HBASE_INPUT_COLUMN']], files=[hasher_fp.name],
                             cmdenvs=cmdenvs, dummy_fp=hasher_fp, **kw)

    def features_to_classifier(self, max_per_label, **kw):
        classifier = sklearn.svm.LinearSVC()
        self._features_to_classifier(classifier, self.feature_class_positive, self.images_table, self.feature_column, self.indoor_class_column, self.models_table, self.feature_classifier_row, self.feature_classifier_column, max_per_label, **kw)
    
    def _features_to_classifier(self, classifier, class_positive, input_table, input_feature_column, input_class_column, output_table, output_row, output_column, max_per_label=None, **kw):
        row_dict = hadoopy_hbase.HBaseRowDict(output_table,
                                              output_column, db=self.hb)
        row_cols = hadoopy_hbase.scanner(self.hb, input_table,
                                         columns=[input_feature_column, input_class_column], **kw)
        label_features = {0: [], 1: []}
        for row, cols in row_cols:
            if max_per_label is not None and len(label_features[0]) >= max_per_label and len(label_features[1]) >= max_per_label:
                break
            label = int(cols[input_class_column] == class_positive)
            if max_per_label is None or len(label_features[label]) < max_per_label:
                print(label)
                print(cols[input_class_column])
                label_features[label].append(cols[input_feature_column])
            else:
                print('Skipping[%d]' % label)
        labels = [0] * len(label_features[0]) + [1] * len(label_features[1])
        features = label_features[0] + label_features[1]
        features_to_classifier(classifier, labels, features)
        cp = picarus.api.Classifier()
        cp.name = '%s-%s-indoor' % (self.images_table, self.feature_name)  # TODO(brandyn): Indoor specific ATM
        cp.feature = json.dumps(self.feature_dict)
        cp.classifier = pickle.dumps(classifier, -1)
        cp.classifier_format = cp.PICKLE
        row_dict[output_row] = cp.SerializeToString()
        print('Train')

    def feature_to_prediction(self):
        classifier = self._get_feature_classifier()
        self._feature_to_prediction(classifier, self.images_table, self.feature_column, self.images_table, self.feature_prediction_column)

    def _feature_to_prediction(self, classifier, input_table, input_column, output_table, output_column, **kw):
        classifier_fp = tempfile.NamedTemporaryFile()
        classifier_fp.write(classifier)
        classifier_fp.flush()
        cmdenvs = {'HBASE_INPUT_COLUMN': input_column,
                   'HBASE_TABLE': input_table,
                   'HBASE_OUTPUT_COLUMN': output_column,
                   'CLASSIFIER_FN': os.path.basename(classifier_fp.name)}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'feature_to_prediction.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[cmdenvs['HBASE_INPUT_COLUMN']], files=[classifier_fp.name],
                             cmdenvs=cmdenvs, dummy_fp=classifier_fp, **kw)

    def get_feature_classifier(self):
        cp = picarus.api.Classifier()
        cp.ParseFromString(self._get_feature_classifier())
        return cp

    def _get_feature_classifier(self):
        out = self.hb.get(self.models_table, self.feature_classifier_row, self.feature_classifier_column)
        if not out:
            raise ValueError('Classifier does not exist!')
        return out[0].value

    def build_feature_index(self):
        si = picarus.api.SearchIndex()
        si.name = '%s-%s' % (self.images_table, self.feature_name)
        si.feature = json.dumps(self.feature_dict)
        si.hash = self._get_feature_hasher()
        si.hash_format = si.PICKLE
        index = image_search.LinearHashDB()
        self._build_index(si, index, self.images_table, self.feature_hash_column, self.class_column, self.models_table, self.feature_index_row, self.feature_index_column)

    def build_masks_index(self):
        si = picarus.api.SearchIndex()
        si.name = '%s-%s' % (self.images_table, 'masks')
        si.feature = pickle.dumps(self._get_texton())
        si.feature_format = si.PICKLE
        si.hash = self._get_mask_hasher()
        si.hash_format = si.PICKLE
        hasher = pickle.loads(si.hash)
        class_params = sorted(hasher.class_params.items(), key=lambda x: [0])
        weights = np.hstack([x[1]['w'] for x in class_params])
        index = image_search.LinearHashJaccardDB(weights)
        self._build_index(si, index, self.images_table, self.masks_hash_column, self.class_column, self.models_table, self.masks_index_row, self.masks_index_column)

    def _build_index(self, si, index, input_table, input_hash_column, input_class_column, output_table, output_row, output_column, **kw):
        row_dict = hadoopy_hbase.HBaseRowDict(output_table,
                                              output_column, db=self.hb)
        row_cols = hadoopy_hbase.scanner(self.hb, input_table,
                                         columns=[input_hash_column, input_class_column], **kw)
        metadata, hashes = zip(*[(json.dumps([cols[input_class_column], base64.b64encode(row)]), cols[input_hash_column])
                                 for row, cols in row_cols])
        row_dict[output_row] = hashes_to_index(si, index, metadata, hashes)

    def _get_texton(self):
        tp = pickle.load(open('tree_ser-texton.pkl'))
        tp2 = pickle.load(open('tree_ser-integral.pkl'))
        return picarus._features.TextonPredict(tp=tp, tp2=tp2, num_classes=9)

    def get_feature_hasher(self):
        return pickle.loads(self._get_feature_hasher())

    def _get_feature_hasher(self):
        out = self.hb.get(self.models_table, self.feature_hasher_row, self.feature_hasher_column)
        if not out:
            raise ValueError('Hasher does not exist!')
        return out[0].value

    def get_masks_hasher(self):
        return pickle.loads(self._get_mask_hasher())

    def _get_mask_hasher(self):
        out = self.hb.get(self.models_table, self.masks_hasher_row, self.masks_hasher_column)
        if not out:
            raise ValueError('Hasher does not exist!')
        return out[0].value

    def _get_feature_index(self):
        out = self.hb.get(self.models_table, self.feature_index_row, self.feature_index_column)
        if not out:
            raise ValueError('Index does not exist!')
        return out[0].value

    def _get_masks_index(self):
        out = self.hb.get(self.models_table, self.masks_index_row, self.masks_index_column)
        if not out:
            raise ValueError('Index does not exist!')
        return out[0].value

if __name__ == '__main__':
    image_retrieval = ImageRetrieval()
    #image_retrieval.create_tables()
    #print image_retrieval.get_hasher()
    #print type(image_retrieval.get_hasher())
    #image_retrieval.image_thumbnail()
    #image_retrieval.image_resize()
    #image_retrieval._feature()
    #image_retrieval._masks()

    #image_retrieval._hash(start_row='sun397train')
    #image_retrieval._hashes()
    #image_retrieval._build_index(start_row='sun397train')

    #image_retrieval._learn_masks_hasher(start_row='sun397train')
    #image_retrieval._mask_hashes()
    #image_retrieval._build_mask_index()

    #image_retrieval.image_resize()
    #image_retrieval.image_thumbnail()
    if 0:
        #image_retrieval.image_to_feature()
        #image_retrieval.image_to_masks()
        #image_retrieval.features_to_hasher(start_row='sun397train', max_rows=100)
        #image_retrieval.masks_to_hasher(start_row='sun397train', max_rows=100)  # TODO implement
        #image_retrieval.feature_to_hash()
        #image_retrieval.masks_to_hash()
        #image_retrieval.build_feature_index()
        #image_retrieval.build_masks_index()
        open('sun397_feature_index.pb', 'w').write(image_retrieval._get_feature_index())
        open('sun397_masks_index.pb', 'w').write(image_retrieval._get_masks_index())
    else:
        # Classifier
        #image_retrieval.features_to_classifier(start_row='sun397train', max_per_label=1000)
        #open('sun397_indoor_classifier.pb', 'w').write(image_retrieval._get_feature_classifier())
        image_retrieval.feature_to_prediction()
