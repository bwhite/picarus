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
import cv2
from confmat import save_confusion_matrix

logging.basicConfig(level=logging.DEBUG)

output_hdfs = 'picarus_temp/%f/' % time.time()


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
        self.texton_classes = json.load(open('class_colors.js'))
        self.texton_num_classes = len(self.texton_classes)
        # Index Settings
        self.class_column = 'meta:class_2'
        self.indoor_class_column = 'meta:class_0'
        self.num_mappers = 6
        #self.versions = self.get_versions()

        # Model columns
        self.model_chunks_column = 'data:model_chunks'
        self.model_column = 'data:model'
        self.input_column = 'data:input'
        self.input_type_column = 'data:input_type'
        self.output_type_column = 'data:output_type'
        self.model_type_column = 'data:model_type'
        self.creation_time_column = 'data:creation_time'
        self.notes_column = 'data:notes'
        self.name_column = 'data:name'
        self.tags_column = 'data:tags'
        self.factory_info_column = 'data:factory_info'

    def get_versions(self):
        return {x: get_version(x) for x in ['picarus', 'imfeat', 'imseg', 'hadoopy', 'impoint', 'hadoopy_hbase']}

    def output_type_to_prefix(self, output_type):
        return {'feature': 'feat:', 'processed_image': 'data:', 'binary_class_confidence': 'pred:', 'multi_class_distance': 'pred:', 'hash': 'hash:', 'index': 'srch:', 'multi_feature': 'mfeat:'}[output_type]

    def input_model_param_to_key(self, input, model, input_type, output_type, email, name, notes='', tags='', factory_info=None):
        assert isinstance(input, str)
        dumps = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':'))
        if isinstance(model, dict):
            model_type = 'json'
            model_str = dumps(model)
        else:
            model_type = 'pickle'
            model_str = dumps(base64.b64encode(zlib.compress(pickle.dumps(model, -1))))
        input_model_str = dumps([input, model_str])
        model_sha1 = hashlib.sha1(input_model_str).digest()
        # Ensures model specifics cannot change, also ensures that name is unique
        prefix = self.output_type_to_prefix(output_type)
        model_key = prefix + model_sha1 + os.urandom(7)

        cols = [hadoopy_hbase.Mutation(column=self.input_column, value=input),
                hadoopy_hbase.Mutation(column=self.input_type_column, value=input_type),
                hadoopy_hbase.Mutation(column=self.output_type_column, value=output_type),
                hadoopy_hbase.Mutation(column=self.model_column, value=model_type),
                hadoopy_hbase.Mutation(column=self.creation_time_column, value=str(time.time())),
                hadoopy_hbase.Mutation(column=self.notes_column, value=notes),
                hadoopy_hbase.Mutation(column=self.name_column, value=name),
                hadoopy_hbase.Mutation(column=self.tags_column, value=tags),
                hadoopy_hbase.Mutation(column='user:' + email, value='rw')]
        if factory_info is not None:
            cols.append(hadoopy_hbase.Mutation(column=self.factory_info_column, value=factory_info))
        chunk_count = 0
        while model_str:
            cols.append(hadoopy_hbase.Mutation(column=self.model_column + '-%d' % chunk_count, value=model_str[:self.max_cell_size]))
            model_str = model_str[self.max_cell_size:]
            print(chunk_count)
            chunk_count += 1
        cols.append(hadoopy_hbase.Mutation(column=self.model_chunks_column, value=np.array(chunk_count, dtype=np.uint32).tostring()))
        self.hb.mutateRow(self.models_table, model_key, cols)
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

    def key_to_model(self, key):
        columns = {x: y.value for x, y in self.hb.getRow(self.models_table, key)[0].columns.items()}
        column_to_name = {}
        names = ['model_chunks', 'input', 'input_type', 'output_type', 'model_type', 'creation_time', 'notes', 'name', 'tags', 'factory_info']
        for name in names:
            column_to_name[getattr(self, name + '_column')] = name
        model_chunks = np.fromstring(columns[self.model_chunks_column], dtype=np.uint32)
        model = []
        for x in range(model_chunks):
            col = self.model_column + '-%d' % x
            model.append(columns[col])
            del columns[col]
        del columns[self.model_chunks_column]
        model = ''.join(model)
        model = json.loads(model)
        if not isinstance(model, dict):
            model = pickle.loads(zlib.decompress(base64.b64decode(model)))
        return model, {column_to_name[k] : v for k, v in columns.items() if k in column_to_name}

    def _model_to_pb(self, pb, model, name):
        if isinstance(model, dict):
            setattr(pb, name, json.dumps(model, separators=(',', ':')))
            setattr(pb, name + '_format', pb.JSON_IMPORT)
        else:
            setattr(pb, name, pickle.dumps(model, -1))
            setattr(pb, name + '_format', pb.PICKLE)

    def key_to_classifier_pb(self, key):
        c = picarus.api.Classifier()
        input, classifier, param = self.key_to_input_model_param(key)
        if param['classifier_type'] == 'sklearn_decision_func':
            c.classifier_type = c.SKLEARN_DECISION_FUNC
        elif param['classifier_type'] == 'class_distance_list':
            c.classifier_type = c.CLASS_DISTANCE_LIST
        else:
            raise ValueError('Unknown classifier type: %s' % param['classifier_type'])
        self._model_to_pb(c, classifier, 'classifier')
        input, feature, param = self.key_to_input_model_param(input['feature'])
        self._model_to_pb(c, feature, 'feature')
        if param['feature_type'] == 'feature':
            c.feature_type = c.FEATURE
        elif param['feature_type'] == 'multi_feature':
            c.feature_type = c.MULTI_FEATURE
        elif param['feature_type'] == 'mask_feature':
            c.feature_type = c.MASK_FEATURE
        else:
            raise ValueError('Unknown feature type: %s' % param['feature_type'])
        input, preprocessor, param = self.key_to_input_model_param(input['processed_image'])
        self._model_to_pb(c, preprocessor, 'preprocessor')
        return c

    def create_tables(self):
        self.hb.createTable(self.models_table, [hadoopy_hbase.ColumnDescriptor('data:')])

    def image_thumbnail(self, **kw):
        # Makes 150x150 thumbnails from the data:image column
        model = {'name': 'picarus.ImagePreprocessor', 'kw': {'method': 'force_square', 'size': 150, 'compression': 'jpg'}}
        self.takeout_link_job(model, 'data:image', 'thum:image_150sq', **kw)

    def image_exif(self, **kw):
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode('meta:exif')}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/image_exif.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=['data:image'], single_value=True,
                             cmdenvs=cmdenvs, **kw)

    def image_preprocessor(self, model_key, **kw):
        model, columns = self.key_to_model(model_key)
        model_fp = picarus.api.model_tofile(model)
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(model_key),
                   'MODEL_FN': os.path.basename(model_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/image_preprocess.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, files=[model_fp.name], columns=[base64.urlsafe_b64decode(columns['input'])], single_value=True,
                             cmdenvs=cmdenvs, dummy_fp=model_fp, **kw)

    def image_to_feature(self, model_key, **kw):
        model, columns = self.key_to_model(model_key)
        model_fp = picarus.api.model_tofile(model)
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(model_key),
                   'MODEL_FN': os.path.basename(model_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/image_to_feature.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, files=[model_fp.name], columns=[base64.urlsafe_b64decode(columns['input'])], single_value=True,
                             jobconfs={'mapred.task.timeout': '6000000'}, cmdenvs=cmdenvs, dummy_fp=model_fp, **kw)

    def takeout_link_job(self, model, input_column, output_column, **kw):
        model_fp = picarus.api.model_tofile(model)
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(output_column),
                   'MODEL_FN': os.path.basename(model_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/takeout_link_job.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, files=[model_fp.name], columns=[input_column], single_value=True,
                             jobconfs={'mapred.task.timeout': '6000000'}, cmdenvs=cmdenvs, dummy_fp=model_fp, **kw)

    def takeout_chain_job(self, model, input_column, output_column, **kw):
        model_fp = picarus.api.model_tofile(model)
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(output_column),
                   'MODEL_FN': os.path.basename(model_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/takeout_chain_job.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, files=[model_fp.name], columns=[input_column], single_value=True,
                             jobconfs={'mapred.task.timeout': '6000000'}, cmdenvs=cmdenvs, dummy_fp=model_fp, **kw)

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

    def features_to_classifier_class_distance_list(self, feature_key, metadata_column, classifier, **kw):
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[feature_key, metadata_column], **kw)
        label_values = ((cols[metadata_column], np.asfarray(picarus.api.np_fromstring(cols[feature_key]))) for _, cols in row_cols)
        classifier.train(label_values)
        feature_input, feature, _ = self.key_to_input_model_param(feature_key)
        classifier_ser = pickle.dumps(classifier, -1)
        print(len(classifier_ser))
        k = image_retrieval.input_model_param_to_key('pred:', input={'feature': feature_key, 'meta': metadata_column},
                                                     model=classifier, param={'classifier_type': 'class_distance_list'})
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
        k = image_retrieval.input_model_param_to_key('pred:', input={'feature': feature_key, 'meta': metadata_column},
                                                     model=classifier, param={'class_positive': class_positive,
                                                                              'classifier_type': 'sklearn_decision_func'})
        print(repr(k))
        return k

    def feature_to_prediction(self, model_key, **kw):
        input_dict, classifier, param, out = self.key_to_input_model_param_output(model_key)
        classifier_fp = picarus.api.model_tofile(classifier)
        classifier_type = 'sklearn_decision_func' if out == 'binary_class_confidence' else 'class_distance_list'
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(model_key),
                   'CLASSIFIER_FN': os.path.basename(classifier_fp.name),
                   'CLASSIFIER_TYPE': classifier_type}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/feature_to_prediction.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[input_dict['feature']], files=[classifier_fp.name], single_value=True,
                             cmdenvs=cmdenvs, dummy_fp=classifier_fp, **kw)

    def hashes_to_index(self, hasher_key, metadata_column, index, **kw):
        hasher_input, hasher, _ = self.key_to_input_model_param(hasher_key)
        feature_input, feature, _ = self.key_to_input_model_param(hasher_input['feature'])
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[hasher_key, metadata_column], **kw)
        metadata, hashes = zip(*[(json.dumps([cols[metadata_column], base64.urlsafe_b64encode(row)]), cols[hasher_key])
                                 for row, cols in row_cols])
        hashes = np.ascontiguousarray(np.asfarray([np.fromstring(h, dtype=np.uint8) for h in hashes]))
        index = index.store_hashes(hashes, np.arange(len(metadata), dtype=np.uint64))
        index.metadata = metadata
        k = image_retrieval.input_model_param_to_key('srch:', input={'hash': hasher_key, 'meta': metadata_column}, model=index)
        print(repr(k))
        return k

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

    def filter_annotations_to_hbase(self):
        import redis
        r = redis.StrictRedis(port=6382, db=6)
        for x in r.keys():
            data = r.hgetall(x)
            print(data)
            user_data = data.get('user_data', 'true') == 'true'
            if not user_data:
                self.hb.deleteAllRow('images', data['image'])

    def filter_batch_annotations_to_hbase(self):
        import redis
        import ast
        r = redis.StrictRedis(port=6382, db=6)
        for x in r.keys():
            v = r.hgetall(x)
            images = map(base64.b64decode, json.loads(v['images']))
            if 'user_data' not in v:
                continue
            user_data = ast.literal_eval(v['user_data'])
            if user_data['polarity'] == 'true':
                # Filter all that are unselected
                for x in user_data['notSelected']:
                    print(repr(images[int(x)]))
                    self.hb.deleteAllRow('images', images[int(x)])
            else:
                # Filter all that are selected
                for x in user_data['selected']:
                    print(repr(images[int(x)]))
                    self.hb.deleteAllRow('images', images[int(x)])

    def _mask_annotation_render(self, row_key, class_segments, image_key, image_superpixel_key, min_votes=1):
        columns = dict((x, y.value) for x, y in self.hb.getRowWithColumns(self.images_table, row_key, [image_key, image_superpixel_key])[0].columns.items())
        image = imfeat.image_fromstring(columns[image_key])
        segments = json.loads(columns[image_superpixel_key])
        class_masks = {}
        class_masks = np.zeros((image.shape[0], image.shape[1], self.texton_num_classes))
        for name, user_segment_groups in class_segments.items():
            cur_mask = np.zeros(image.shape[:2], dtype=np.uint8)
            segment_counts = {}
            for x in sum(user_segment_groups, []):
                try:
                    segment_counts[x] += 1
                except KeyError:
                    segment_counts[x] = 1
            valid_segments = [x for x, y in segment_counts.items() if y >= min_votes]
            for user_segment in valid_segments:
                hull = segments[user_segment]
                hull = np.asarray(hull).astype(np.int32).reshape(1, -1, 2)
                mask_color = 255
                cv2.drawContours(cur_mask, hull, -1, mask_color, -1)
                cv2.drawContours(cur_mask, hull, -1, mask_color, 2)
            class_masks[:, :, self.texton_classes[name]['mask_num']] = cur_mask / 255.
        return class_masks, image

    def _filter_mask_annotations(self, response, min_annotation_time=10.):
        try:
            annotation_time = float(response['end_time']) - float(response['start_time'])
        except KeyError:
            return True
        else:
            if annotation_time < min_annotation_time:
                return True
        return False

    def annotation_masks_to_disk(self, image_key, image_superpixel_key):
        import redis
        import ast
        import imfeat
        import cv2
        u = redis.StrictRedis(port=6381, db=0)
        r = redis.StrictRedis(port=6381, db=6)
        responses = [r.hgetall(x) for x in r.keys()]
        print('Total Responses[%d]' % len(responses))
        class_num_to_name = {y['mask_num']: x for x, y in self.texton_classes.items()}
        for x in responses:
            if 'user_data' in x:
                user = u.hgetall(x['user_id'])
                worker_id = user.get('workerId', '00NOID')
                print((x['user_id'], user))
                x['user_data'] = ast.literal_eval(x['user_data'])
                if self._filter_mask_annotations(x):
                    print('Filtering annotation')
                    continue
                if x['user_data']['segments']:
                    row_key = x['image']
                    class_masks, image = self._mask_annotation_render(row_key, {x['user_data']['name']: [x['user_data']['segments']]}, image_key, image_superpixel_key)
                    class_masks = (class_masks * 255).astype(np.uint8)
                    print(x)
                    print('Storing row [%s]' % repr(row_key))
                    for x in np.sum(class_masks.reshape((-1, class_masks.shape[-1])), 0).nonzero()[0]:
                        fn = 'images/%s_%s_%s' % (class_num_to_name[x], base64.b64encode(row_key), worker_id)
                        print(fn)
                        cur_mask = np.ascontiguousarray(class_masks[:, :, x])
                        cv2.imwrite(fn + '_0.png', cur_mask)
                        cv2.imwrite(fn + '_1.jpg', image)
                    #class_masks_ser = picarus.api.np_tostring(class_masks)
                    #self.hb.mutateRow(self.images_table, row_key, [hadoopy_hbase.Mutation(column=self.masks_gt_column, value=class_masks_ser)])

    def annotation_masks_to_hbase(self, image_key, image_superpixel_key, masks_gt_column='feat:masks_gt', min_votes=2):
        import redis
        import ast
        import imfeat
        import cv2
        r = redis.StrictRedis(port=6381, db=6)
        responses = [r.hgetall(x) for x in r.keys()]
        print('Total Responses[%d]' % len(responses))
        image_class_segments = {}  # [row][class_name] = segments
        class_num_to_name = {y['mask_num']: x for x, y in self.texton_classes.items()}
        for x in responses:
            if 'user_data' in x:
                x['user_data'] = ast.literal_eval(x['user_data'])
                if self._filter_mask_annotations(x):
                    continue
                if x['user_data']['segments']:
                    image_class_segments.setdefault(x['image'], {}).setdefault(x['user_data']['name'], []).append(x['user_data']['segments'])
        for row_key, class_segments in image_class_segments.items():
            class_masks, image = self._mask_annotation_render(row_key, class_segments, image_key, image_superpixel_key, min_votes=min_votes)
            class_masks_ser = picarus.api.np_tostring(class_masks)
            class_masks = (class_masks * 255).astype(np.uint8)
            for x in np.sum(class_masks.reshape((-1, class_masks.shape[-1])), 0).nonzero()[0]:
                fn = 'images/%s_%s' % (class_num_to_name[x], base64.b64encode(row_key))
                print(fn)
                cur_mask = np.ascontiguousarray(class_masks[:, :, x])
                cv2.imwrite(fn + '_0.png', cur_mask)
                cv2.imwrite(fn + '_1.jpg', image)
            print('Storing row [%s]' % repr(row_key))
            self.hb.mutateRow(self.images_table, row_key, [hadoopy_hbase.Mutation(column=masks_gt_column, value=class_masks_ser)])

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

    def evaluate_classifier_class_distance_list(self, classifier_key, **kw):
        classifier = picarus.api.feature_classifier_frompb(self.key_to_classifier_pb(classifier_key))
        input_dict = self.key_to_input_model_param(classifier_key)[0]
        feature_key = input_dict['feature']
        metadata_key = input_dict['meta']
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[feature_key, metadata_key], **kw)
        cm = {}  # [true][pred]
        total = 0
        correct = 0
        for row, columns in row_cols:
            feature = picarus.api.np_fromstring(columns[feature_key])
            print(feature.shape)
            c = classifier(feature)
            print(c)
            total += 1
            try:
                pred_class = c[0]['class']
            except IndexError:
                pred_class = ''
            true_class = columns[metadata_key]
            if pred_class == true_class:
                correct += 1
            try:
                cm.setdefault(true_class, {})[pred_class] += 1
            except KeyError:
                cm.setdefault(true_class, {})[pred_class] = 1
            print(cm)
            print(correct / float(total))
        print(correct / float(total))
        return {'cm': cm, 'total': total, 'correct': correct}

    def image_to_superpixels(self, input_table, input_column, output_column, **kw):
        cmdenvs = {'HBASE_TABLE': input_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(output_column)}
        hadoopy_hbase.launch(input_table, output_hdfs + str(random.random()), 'hadoop/image_to_superpixels.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=[input_column], single_value=True,
                             cmdenvs=cmdenvs, jobconfs={'mapred.task.timeout': '6000000'}, **kw)

    def model_to_name(self, model):
        args = list(model.get('args', []))
        for x, y in sorted(model.get('kw', {}).items()):
            y = repr(y)
            if len(y) > 20:
                y = 'sha1:' + repr(hashlib.sha1(y).hexdigest())
            args.append('%s=%s' % (x, y))
        return model['name'] + '(%s)' % ', '.join(args)


if __name__ == '__main__':
    image_retrieval = PicarusManager()
    #image_retrieval.create_tables()

    def _model_to_name(model):
        return image_retrieval.model_to_name(model)

    def run_preprocessor(k, **kw):
        image_retrieval.image_preprocessor(k, **kw)

    def create_preprocessor(model):
        k = image_retrieval.input_model_param_to_key('data:', input={'image': 'data:image'}, model=model, name=_model_to_name(model))
        print(repr(k))
        return k

    def run_feature(k, **kw):
        image_retrieval.image_to_feature(k, **kw)

    def create_feature(image_key, model):
        print(_model_to_name(model))
        k = image_retrieval.input_model_param_to_key('feat:', input={'image': image_key}, model=model, param={'feature_type': 'feature'}, name=_model_to_name(model))
        print(repr(k))
        return k

    def create_mask_feature(image_key, model, **kw):
        k = image_retrieval.input_model_param_to_key('mask:', input={'image': image_key}, model=model, param={'feature_type': 'mask_feature'})
        print(repr(k))
        return k

    def create_multi_feature(image_key, model):
        print(_model_to_name(model))
        k = image_retrieval.input_model_param_to_key('mfeat:', input={'image': image_key}, model=model, param={'feature_type': 'multi_feature'}, name=_model_to_name(model))
        print(repr(k))
        return k

    def run_hasher(k, **kw):
        image_retrieval.feature_to_hash(k, **kw)

    def create_hasher(feature_key, hasher, **kw):
        k = image_retrieval.features_to_hasher(feature_key, hasher, **kw)
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


    # SUN397 Feature/Classifier/Hasher/Index
    start_row = 'sun397:'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    image_key = create_preprocessor({'name': 'imfeat.ImagePreprocessor', 'kw': {'method': 'max_side', 'size': 320, 'compression': 'jpg'}})
    #run_preprocessor(image_key, start_row=start_row, stop_row=stop_row)
    feature_key = create_feature(image_key, {'name': 'picarus._features.HOGBoVW', 'kw': {'clusters': json.load(open('clusters.js')), 'levels': 2, 'sbin': 16, 'blocks': 1}})
    #run_feature(feature_key, start_row=start_row, stop_row=stop_row)

    start_row = 'sun397:train'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    hasher_key = create_hasher(feature_key, image_search.RRMedianHasher(hash_bits=256, normalize_features=False), start_row=start_row, stop_row=stop_row)

    start_row = 'sun397:'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    run_hasher(hasher_key, start_row=start_row, stop_row=stop_row)

    start_row = 'sun397:train'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    create_index(hasher_key, 'meta:class_2', image_search.LinearHashDB(), start_row=start_row, stop_row=stop_row)
    quit()
    classifier_key = create_classifier_sklearn_decision_func(feature_key, 'meta:class_0', 'indoor', sklearn.svm.LinearSVC(), start_row=start_row, stop_row=stop_row)
    print(repr(classifier_key))


    start_row = 'sun397:'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    run_classifier(classifier_key, start_row=start_row, stop_row=stop_row)
    quit()


    # Landmarks
    start_row = 'landmarks:flickr'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    #image_key = create_preprocessor({'name': 'imfeat.ImagePreprocessor', 'kw': {'method': 'max_side', 'size': 500, 'compression': 'jpg'}})
    image_key = create_preprocessor({'name': 'imfeat.ImagePreprocessor', 'kw': {'method': 'max_side', 'size': 80, 'compression': 'jpg'}})
    run_preprocessor(image_key, start_row=start_row, stop_row=stop_row)
    #feature_key = create_multi_feature(image_key, {'name': 'imfeat.HOGLatent', 'kw': {'sbin': 64}})
    #feature_key = create_multi_feature(image_key, {'name': 'picarus.modules.SURF'})
    feature_key = create_multi_feature(image_key, {'name': 'picarus.modules.ImageBlocks', 'kw': {'sbin': 16, 'mode': 'lab', 'num_sizes': 3}})
    run_feature(feature_key, start_row=start_row, stop_row=stop_row)

    stop_row = start_row + chr(204)
    classifier_key = create_classifier_class_distance_list(feature_key, 'meta:class', picarus.modules.LocalNBNNClassifier(), start_row=start_row, stop_row=stop_row)

    # Evaluate landmarks
    start_row = 'landmarks:flickr'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    start_row = 'landmarks:flickr' + chr(204)
    image_retrieval.evaluate_classifier_class_distance_list(classifier_key, start_row=start_row, stop_row=stop_row)
    quit()


    # Logo
    start_row = 'logos:google'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    image_key = create_preprocessor({'name': 'imfeat.ImagePreprocessor', 'kw': {'method': 'max_side', 'size': 80, 'compression': 'jpg'}})
    run_preprocessor(image_key, start_row=start_row, stop_row=stop_row)
    feature_key = create_multi_feature(image_key, {'name': 'picarus.modules.ImageBlocks', 'kw': {'sbin': 16, 'mode': 'lab', 'num_sizes': 3}})
    run_feature(feature_key, start_row=start_row, stop_row=stop_row)

    stop_row = start_row + chr(204)
    classifier_key = create_classifier_class_distance_list(feature_key, 'meta:class', picarus.modules.LocalNBNNClassifier(), start_row=start_row, stop_row=stop_row)

    # Evaluate Logos
    start_row = 'logos:google'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    start_row = 'logos:google' + chr(204)
    image_retrieval.evaluate_classifier_class_distance_list(classifier_key, start_row=start_row, stop_row=stop_row)
    quit()


    image_key = create_preprocessor({'name': 'imfeat.ImagePreprocessor', 'kw': {'method': 'force_max_side', 'size': 320, 'compression': 'jpg'}})
    image_retrieval.annotation_masks_to_hbase(image_key, 'feat:superpixel')
    quit()


    start_row = 'sun397:'
    stop_row = start_row[:-1] + chr(ord(start_row[-1]) + 1)
    print(image_key)
    #run_preprocessor(image_key, start_row=start_row, stop_row=stop_row)
    #image_retrieval.image_to_superpixels('images', image_key, 'feat:superpixel', start_row=start_row, stop_row=stop_row)
    quit()
    if 0:
        # TODO: 1.) Run superpixel segmentation, 2.) Write annotation masks to hbase, 3.) Put data on hbase (imseg), 4.) Run tree-level (imseg)
        image_key = create_preprocessor({'name': 'imfeat.ImagePreprocessor', 'kw': {'method': 'force_max_side', 'size': 320, 'compression': 'jpg'}})
        image_retrieval.annotation_masks_to_hbase(image_key, 'sdfsdfs')
        quit()


    # Masks
    #feature_key = create_mask_feature(image_key, image_retrieval._get_texton(base64.b64decode('cHJlZDqOWGdqIgoVV27QmARQoqxb15Y+9A==')))
    #run_feature(feature_key, start_row='sun397:', stop_row='sun398:')
