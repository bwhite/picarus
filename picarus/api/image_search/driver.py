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
from confmat import save_confusion_matrix

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
        #self.feature_dict = {'name': 'imfeat.GIST'}
        #self.feature_name = 'gist'
        #self.feature_dict = {'name': 'imfeat.PyramidHistogram', 'args': ['lab'], 'kw': {'levels': 2, 'num_bins': [4, 11, 11]}}
        #self.feature_name = 'lab_pyramid_histogram_2level_4_11_11'
        self.feature_dict = {'name': 'picarus._features.HOGBoVW', 'kw': {'clusters': json.load(open('clusters.js')), 'levels': 2, 'sbin': 16, 'blocks': 1}}
        self.feature_name = 'bovw_hog_levels2_sbin16_blocks1_clusters100'
        self.superpixel_column = 'feat:superpixel'
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
        self.texton_num_classes = 8
        self.texton_classes = json.load(open('../class_colors.js'))
        self.masks_hasher_row = 'masks'
        self.masks_hasher_column = 'data:hasher_masks'
        self.masks_hash_column = 'hash:masks'
        self.masks_ilp_column = 'hash:masks_ilp'
        # Index Settings
        self.feature_index_row = self.images_table
        self.feature_index_column = 'data:index_' + self.feature_name
        self.masks_index_row = 'masks'
        self.masks_index_column = 'data:index_masks'
        self.masks_column = 'feat:masks'
        self.masks_gt_column = 'feat:masks_gt'
        self.class_column = 'meta:class_2'
        self.indoor_class_column = 'meta:class_0'
        self.num_mappers = 10

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

    def image_to_superpixels(self):
        self._image_to_superpixels(self.images_table, self.image_column, self.images_table, self.superpixel_column)

    def _image_to_superpixels(self, input_table, input_column, output_table, output_column):
        cmdenvs = {'HBASE_INPUT_COLUMN': input_column,
                   'HBASE_TABLE': output_table,
                   'HBASE_OUTPUT_COLUMN': output_column}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'image_to_superpixels.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs, jobconfs={'mapred.task.timeout': '6000000'})

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

    def masks_to_ilp(self, **kw):
        self._masks_to_ilp(self.images_table, self.masks_column, self.masks_ilp_column, **kw)

    def _masks_to_ilp(self, input_table, input_column, output_column, **kw):
        cmdenvs = {'HBASE_INPUT_COLUMN': input_column,
                   'HBASE_TABLE': input_table,
                   'HBASE_OUTPUT_COLUMN': output_column}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'masks_to_ilp.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs, **kw)

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
        if isinstance(classifier, dict):
            cp.feature = json.dumps(self.feature_dict)
            cp.feature_format = cp.JSON_IMPORT
        else:
            cp.feature = pickle.dumps(self.feature_dict, -1)
            cp.feature_format = cp.PICKLE
            
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
        tp = pickle.load(open('../tree_ser-texton.pkl'))
        tp2 = pickle.load(open('../tree_ser-integral.pkl'))
        return picarus._features.TextonPredict(tp=tp, tp2=tp2, num_classes=self.texton_num_classes)

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

    def evaluate_masks(self, cm_ilp):
        # Go through each mask and compare it to the annotation results
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[self.masks_gt_column])
        cms = {'train': np.zeros((self.texton_num_classes, self.texton_num_classes), dtype=np.int32),
               'test': np.zeros((self.texton_num_classes, self.texton_num_classes), dtype=np.int32)}
        ilps = []
        if cm_ilp:
            ilp_weights = json.load(open('ilp_weights.js'))  # load weights from previous run
            ilp_weights['ilp_tables'] = np.asfarray(ilp_weights['ilp_tables'])
        for row, columns in row_cols:
            gt = picarus.api.np_fromstring(columns[self.masks_gt_column])
            ilp_pred = np.fromstring(self.hb.get(self.images_table, row, self.feature_prediction_column)[0].value, dtype=np.double)[0]
            print(ilp_pred)
            masks = picarus.api.np_fromstring(self.hb.get(self.images_table, row, self.masks_column)[0].value)
            if cm_ilp:
                try:
                    bin_index = [x for x, y in enumerate(ilp_weights['bins']) if y >= ilp_pred][0]
                except IndexError:
                    bin_index = ilp_weights['ilp_tables'].shape[1]
                if bin_index != 0:
                    bin_index -= 1
                print('bin_index[%d]' % bin_index)
                masks *= ilp_weights['ilp_tables'][:, bin_index]
            masks_argmax = np.argmax(masks, 2)
            gt_sums = np.sum(gt.reshape(-1, gt.shape[2]), 0).tolist()
            print(gt_sums)
            if row.startswith('sun397train'):
                cm = cms['train']
                ilps.append({'gt_sums': gt_sums, 'ilp_pred': ilp_pred, 'gt_size': gt.shape[0] * gt.shape[1]})
            else:
                cm = cms['test']
            for mask_num in range(gt.shape[2]):
                if not np.any(gt[:, :, mask_num]):
                    continue
                print(mask_num)
                #print (gt[:, :, mask_num] > 0).nonzero()
                preds = masks_argmax[(gt[:, :, mask_num] > 0).nonzero()]
                h, bins = np.histogram(preds, np.arange(self.texton_num_classes + 1))
                np.testing.assert_equal(bins, np.arange(self.texton_num_classes + 1))
                cm[mask_num] += h
            json.dump({'cms': {'train': cms['train'].tolist(), 'test': cms['test'].tolist()}, 'cm_ilp': cm_ilp, 'ilps': ilps}, open('eval.js', 'w'))
            for split in ['train', 'test']:
                cm = cms[split]
                print(split)
                print(cm)
                if np.any(cm):
                    print(((cm / float(np.sum(cm))) * 100).astype(np.int32))
        classes = [z[1] for z in sorted([(y['mask_num'], x) for x, y in self.texton_classes.items()])]
        title_suffix = 'w ilp)' if cm_ilp else 'w/o ilp)'
        fn_suffix = '_ilp.png' if cm_ilp else '.png'
        save_confusion_matrix(cms['test'], classes, 'confmat_test' + fn_suffix, title='Confusion Matrix (test ' + title_suffix)
        save_confusion_matrix(cms['train'], classes, 'confmat_train' + fn_suffix, title='Confusion Matrix (train ' + title_suffix)

    def evaluate_masks_stats(self):
        data = json.load(open('eval.js'))
        ilps = data['ilps']
        class_ilps = [[] for x in range(self.texton_num_classes)]
        ilp_preds = []
        for x in ilps:
            for y, z in enumerate(np.array(x['gt_sums']) / float(x['gt_size'])):
                class_ilps[y].append((x['ilp_pred'], z))
            ilp_preds.append(x['ilp_pred'])
        for x in class_ilps:
            x.sort()

        # Make ilp bins (roughly equal # of items each)
        ilp_preds.sort()
        num_ilp_bins = 5
        elements_per_bin = int(np.round(len(ilp_preds) / num_ilp_bins))
        bins = []
        for x in range(num_ilp_bins + 1):
            bins.append(ilp_preds[x * elements_per_bin])

        mask_num_to_class = dict((y['mask_num'], x) for x, y in self.texton_classes.items())
        ilp_tables = []
        for y, x in enumerate(class_ilps):
            ilp_confs, class_probs = zip(*x)
            weighted_counts, bins2 = np.histogram(ilp_confs, bins, weights=class_probs)
            counts, bins3 = np.histogram(ilp_confs, bins)
            if y == 0:
                print 'bin_counts', counts
            ilp_tables.append((weighted_counts.astype(np.double) / counts).tolist())
            print mask_num_to_class[y], ilp_tables[-1]
        json.dump({'ilp_tables': ilp_tables, 'bins': bins}, open('ilp_weights.js', 'w'))
        print(len(ilps))
        print(ilps[0])

    def evaluate_nbnn(self):
        c = picarus.modules.LocalNBNNClassifier(10, 16, num_points=1000, scale=1)

        def inner(num_rows, **kw):
            row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                             columns=[self.image_column, self.indoor_class_column], **kw)
            for x, (_, cols) in enumerate(row_cols):
                print(repr(x))
                if x >= num_rows:
                    break
                yield cols[self.indoor_class_column], imfeat.image_fromstring(cols[self.image_column])
        c.train(inner(5000, start_row='sun397train'))
        cms = {}
        for cur_class, image in inner(100):
            pred_class = c.analyze(image)[0]['class']
            try:
                cms.setdefault(cur_class, {})[pred_class] += 1
            except KeyError:
                cms[cur_class][pred_class] = 1
            print cur_class, pred_class
        print(cms)


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
    #image_retrieval.annotation_masks_to_hbase()
    #image_retrieval.evaluate_masks(False)
    #image_retrieval.evaluate_masks_stats()
    #image_retrieval.evaluate_nbnn()
    #image_retrieval.cluster_points_local(max_rows=1000)
    #quit()
    if 1:
        image_retrieval.image_to_feature()
        #image_retrieval.image_to_masks()
        image_retrieval.features_to_hasher(start_row='sun397train', max_rows=1000)
        #image_retrieval.masks_to_hasher(start_row='sun397train', max_rows=1000)
        image_retrieval.feature_to_hash()
        #image_retrieval.masks_to_hash()
        image_retrieval.build_feature_index()
        #image_retrieval.build_masks_index()
        open('sun397_feature_index.pb', 'w').write(image_retrieval._get_feature_index())
        #open('sun397_masks_index.pb', 'w').write(image_retrieval._get_masks_index())
        # Classifier
        image_retrieval.features_to_classifier(start_row='sun397train', max_per_label=5000)
        open('sun397_indoor_classifier.pb', 'w').write(image_retrieval._get_feature_classifier())
        image_retrieval.feature_to_prediction()
        image_retrieval.prediction_to_conf_gt(stop_row='sun397train')
    #image_retrieval.image_to_superpixels()
    #image_retrieval.masks_to_ilp()
