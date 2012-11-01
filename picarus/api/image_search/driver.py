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
logging.basicConfig(level=logging.DEBUG)

#a = hadoopy_hbase.connect()
#for x in hadoopy_hbase.scanner(a, 'sun397'):
#    break

output_hdfs = 'picarus_temp/%f/' % time.time()


def masks_to_hasher(masks, hash_bits):
    masks_iter = (pickle.loads(x) for x in itertools.islice(masks, 100))
    out = image_search.HIKHasherGreedy(hash_bits=hash_bits).train(masks_iter)
    masks_iter = (pickle.loads(x) for x in itertools.islice(masks, 100))
    out_masks = np.array([out(masks) for masks in masks_iter])
    print(out_masks.shape)
    print(out_masks)
    return pickle.dumps(out, -1)


def mask_hashes_to_index(metadata, hashes, si):
    hasher = pickle.loads(si.hash)
    class_params = sorted(hasher.class_params.items(), key=lambda x: [0])
    weights = np.hstack([x[1]['w'] for x in class_params])
    hashes = np.ascontiguousarray([np.fromstring(h, dtype=np.uint8) for h in hashes])
    si.metadata.extend(metadata)
    index = image_search.LinearHashJaccardDB(weights).store_hashes(hashes, np.arange(len(metadata), dtype=np.uint64))
    si.index = pickle.dumps(index, -1)
    si.index_format = si.PICKLE
    return si.SerializeToString()


class ImageRetrieval(object):
    
    def __init__(self):
        self.images_orig_column = 'data:image'
        self.images_column = 'data:image_320'
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
        self.hasher_row = self.images_table
        self.hasher_column = 'data:hasher_' + self.feature_name
        self.hb = hadoopy_hbase.connect()
        self.hash_column = 'hash:' + self.feature_name
        # Mask Hasher settings
        self.masks_hasher_row = 'masks'
        self.masks_hasher_column = 'data:hasher_masks'
        self.masks_hash_column = 'hash:masks'
        # Index Settings
        self.index_row = self.images_table
        self.index_column = 'data:index_' + self.feature_name
        self.masks_index_row = 'masks'
        self.masks_index_column = 'data:index_masks'
        self.masks_column = 'feat:masks'
        self.class_column = 'meta:class_2'

    def create_tables(self):
        self.hb.createTable(self.models_table, [hadoopy_hbase.ColumnDescriptor('data:')])

    def _clean_images(self):
        cmdenvs = {'HBASE_INPUT_COLUMN': self.images_orig_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.images_column}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'image_clean.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=4, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs)

    def _thumbnail_images(self):
        cmdenvs = {'HBASE_INPUT_COLUMN': self.images_orig_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.thumbnails_column}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'image_thumbnail.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=4, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs)


    def _feature(self):
        feature_fp = self._tempfile(zlib.compress(json.dumps(self.feature_dict)), suffix='.gz')
        cmdenvs = {'HBASE_INPUT_COLUMN': self.images_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.feature_column,
                   'FEATURE_FN': os.path.basename(feature_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'image_to_feature.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=6, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs, files=[feature_fp.name])

    def _masks(self):
        cmdenvs = {'HBASE_INPUT_COLUMN': self.images_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.masks_column}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'image_to_masks.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=4, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs, files=['tree_ser-texton.pkl', 'tree_ser-integral.pkl'],
                             jobconfs={'mapred.task.timeout': '6000000'})

    def _hash(self, **kw):
        cmdenvs = {'HASH_BITS': 256,
                   'HBASE_INPUT_COLUMN': self.feature_column,
                   'HBASE_OUTPUT_ROW': self.hasher_row,
                   'HBASE_OUTPUT_TABLE': self.models_table,
                   'HBASE_OUTPUT_COLUMN': self.hasher_column}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'features_to_hasher.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=2, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs, **kw)

    def _learn_masks_hasher(self, **kw):
        row_dict = hadoopy_hbase.HBaseRowDict(self.models_table,
                                              self.masks_hasher_column, db=self.hb)
        masks = hadoopy_hbase.scanner_column(self.hb, self.images_table,
                                             self.masks_column, **kw)
        row_dict[self.masks_hasher_row] = masks_to_hasher(masks, 8)

    def _tempfile(self, data, suffix=''):
        fp = tempfile.NamedTemporaryFile(suffix=suffix)
        fp.write(data)
        fp.flush()
        return fp

    def _hashes(self, **kw):
        hashes_fp = self._tempfile(self._get_hasher(), suffix='.pkl')
        cmdenvs = {'HBASE_INPUT_COLUMN': self.feature_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.hash_column,
                   'HASHER_FN': os.path.basename(hashes_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'features_to_hashes.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=2, columns=[cmdenvs['HBASE_INPUT_COLUMN']], files=[hashes_fp.name],
                             cmdenvs=cmdenvs, **kw)

    def _mask_hashes(self, **kw):
        hashes_fp = self._tempfile(self._get_mask_hasher(), suffix='.pkl')
        cmdenvs = {'HBASE_INPUT_COLUMN': self.masks_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.masks_hash_column,
                   'HASHER_FN': os.path.basename(hashes_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'masks_to_hashes.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=2, columns=[cmdenvs['HBASE_INPUT_COLUMN']], files=[hashes_fp.name],
                             cmdenvs=cmdenvs, **kw)

    def _build_index(self, **kw):
        si = picarus.api.SearchIndex()
        si.name = '%s-%s' % (self.images_table, self.feature_name)
        si.feature = json.dumps(self.feature_dict)
        si.hash = self._get_hasher()
        si.hash_format = si.PICKLE
        index_fp = self._tempfile(si.SerializeToString())
        cmdenvs = {'HBASE_INPUT_COLUMN': self.hash_column,
                   'HBASE_CLASS_COLUMN': self.class_column,
                   'HBASE_OUTPUT_ROW': self.index_row,
                   'HBASE_OUTPUT_TABLE': self.models_table,
                   'HBASE_OUTPUT_COLUMN': self.index_column,
                   'INDEX_FN': os.path.basename(index_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hashes_to_index.py',
                             libjars=['hadoopy_hbase.jar'],
                             num_mappers=2, columns=[cmdenvs['HBASE_INPUT_COLUMN'], cmdenvs['HBASE_CLASS_COLUMN']],
                             files=[index_fp.name],
                             cmdenvs=cmdenvs, **kw)

    def _build_mask_index(self, **kw):
        si = picarus.api.SearchIndex()
        si.name = '%s-%s' % (self.images_table, 'masks')
        tp = pickle.load(open('tree_ser-texton.pkl'))
        tp2 = pickle.load(open('tree_ser-integral.pkl'))
        si.feature = pickle.dumps(picarus._features.TextonPredict(tp=tp, tp2=tp2, num_classes=9))
        si.feature_format = si.PICKLE
        si.hash = self._get_mask_hasher()
        si.hash_format = si.PICKLE
        row_dict = hadoopy_hbase.HBaseRowDict(self.models_table,
                                              self.masks_index_column, db=self.hb)
        row_cols = hadoopy_hbase.scanner(self.hb, self.images_table,
                                         columns=[self.masks_hash_column, self.class_column], **kw)
        print('Got scanner')
        metadata, hashes = zip(*[(json.dumps([cols[self.class_column], base64.b64encode(row)]), cols[self.masks_hash_column]) for row, cols in row_cols])
        print('Got metadata/hashes')
        row_dict[self.masks_hasher_row] = mask_hashes_to_index(metadata, hashes, si)

    def get_hasher(self):
        return pickle.loads(self._get_hasher())

    def _get_hasher(self):
        out = self.hb.get(self.models_table, self.hasher_row, self.hasher_column)
        if not out:
            raise ValueError('Hasher does not exist!')
        return out[0].value

    def get_mask_hasher(self):
        return pickle.loads(self._get_mask_hasher())

    def _get_mask_hasher(self):
        out = self.hb.get(self.models_table, self.masks_hasher_row, self.masks_hasher_column)
        if not out:
            raise ValueError('Hasher does not exist!')
        return out[0].value

    def _get_index(self):
        out = self.hb.get(self.models_table, self.index_row, self.index_column)
        if not out:
            raise ValueError('Index does not exist!')
        return out[0].value

    def _get_mask_index(self):
        out = self.hb.get(self.models_table, self.masks_index_row, self.masks_index_column)
        if not out:
            raise ValueError('Index does not exist!')
        return out[0].value

if __name__ == '__main__':
    image_retrieval = ImageRetrieval()
    #image_retrieval.create_tables()
    #print image_retrieval.get_hasher()
    #print type(image_retrieval.get_hasher())

    #image_retrieval._thumbnail_images()
    
    #image_retrieval._clean_images()
    #image_retrieval._feature()
    #image_retrieval._masks()

    #image_retrieval._hash(start_row='sun397train')
    #image_retrieval._hashes()
    #image_retrieval._build_index(start_row='sun397train')
    
    #open('sun397_index.pb', 'w').write(image_retrieval._get_index())
    #image_retrieval._learn_masks_hasher(start_row='sun397train')
    #image_retrieval._mask_hashes()
    image_retrieval._build_mask_index()
    open('sun397_mask_index.pb', 'w').write(image_retrieval._get_mask_index())
