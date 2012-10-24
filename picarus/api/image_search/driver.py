
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
logging.basicConfig(level=logging.DEBUG)

a = hadoopy_hbase.connect()
for x in hadoopy_hbase.scanner(a, 'sun397'):
    break

output_hdfs = 'picarus_temp/%f/' % time.time()

# TODO: Check image retrieval/logo search/mask modules and consolidate here


class ImageRetrieval(object):
    
    def __init__(self):
        self.images_orig_column = 'data:image'
        self.images_column = 'data:image_clean'
        self.images_table = 'sun397'
        self.models_table = 'picarus_models'
        # Feature Settings
        self.feature_dict = {'name': 'imfeat.GIST'}
        self.feature_name = 'gist'
        #self.feature_dict = {'name': 'imfeat.PyramidHistogram', 'args': ['lab'], 'kw': {'levels': 3, 'num_bins': [4, 11, 11]}}
        #self.feature_name = 'lab_pyramid_histogram_3level_4_11_11'
        self.feature_column = 'data:feature_' + self.feature_name
        # Hasher settings
        self.hasher_row = self.images_table
        self.hasher_column = 'data:hasher_' + self.feature_name
        self.hb = hadoopy_hbase.connect()
        self.hash_column = 'data:hash_' + self.feature_name
        # Index Settings
        self.index_row = self.images_table
        self.index_column = 'data:index_' + self.feature_name

    def create_tables(self):
        self.hb.createTable(self.models_table, [hadoopy_hbase.ColumnDescriptor('data:')])

    def _clean_images(self):
        cmdenvs = {'HBASE_INPUT_COLUMN': self.images_orig_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.images_column}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'image_clean.py', libjars=['hadoopy_hbase.jar'],
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

    def _hash(self):
        cmdenvs = {'HASH_BITS': 128,
                   'HBASE_INPUT_COLUMN': self.feature_column,
                   'HBASE_OUTPUT_ROW': self.hasher_row,
                   'HBASE_OUTPUT_TABLE': self.models_table,
                   'HBASE_OUTPUT_COLUMN': self.hasher_column}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'features_to_hasher.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=4, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             cmdenvs=cmdenvs)

    def _tempfile(self, data, suffix=''):
        fp = tempfile.NamedTemporaryFile(suffix=suffix)
        fp.write(data)
        fp.flush()
        return fp

    def _hashes(self):
        hashes_fp = self._tempfile(self._get_hasher(), suffix='.pkl')
        cmdenvs = {'HBASE_INPUT_COLUMN': self.feature_column,
                   'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': self.hash_column,
                   'HASHER_FN': os.path.basename(hashes_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'features_to_hashes.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=4, columns=[cmdenvs['HBASE_INPUT_COLUMN']], files=[hashes_fp.name],
                             cmdenvs=cmdenvs)

    def _build_index(self):
        si = picarus.api.SearchIndex()
        si.name = '%s-%s' % (self.images_table, self.feature_name)
        si.feature = json.dumps(self.feature_dict)
        si.hash = self._get_hasher()
        si.hash_format = si.PICKLE
        index_fp = self._tempfile(si.SerializeToString())
        cmdenvs = {'HBASE_INPUT_COLUMN': self.hash_column,
                   'HBASE_OUTPUT_ROW': self.index_row,
                   'HBASE_OUTPUT_TABLE': self.models_table,
                   'HBASE_OUTPUT_COLUMN': self.index_column,
                   'INDEX_FN': os.path.basename(index_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hashes_to_index.py',
                             libjars=['hadoopy_hbase.jar'],
                             num_mappers=4, columns=[cmdenvs['HBASE_INPUT_COLUMN']],
                             files=[index_fp.name],
                             cmdenvs=cmdenvs)


    def _query_index(self):
        pass

    def get_hasher(self):
        return pickle.loads(self._get_hasher())

    def _get_hasher(self):
        out = self.hb.get(self.models_table, self.hasher_row, self.hasher_column)
        if not out:
            raise ValueError('Hasher does not exist!')
        return out[0].value

    def _get_index(self):
        out = self.hb.get(self.models_table, self.index_row, self.index_column)
        if not out:
            raise ValueError('Index does not exist!')
        return out[0].value

    def learn(self):
        # feature
        self._feature()
        # learn hash

    def build(self):
        # feature
        # hash
        # build index
        pass

    def search(self):
        # feature
        # hash
        # query index
        pass

image_retrieval = ImageRetrieval()
#image_retrieval.create_tables()
#image_retrieval._hash()
#print image_retrieval.get_hasher()
#print type(image_retrieval.get_hasher())
#image_retrieval._hashes()
#image_retrieval._build_index()
open('sun397_gist_index.pb', 'w').write(image_retrieval._get_index())
#image_retrieval._feature()
#image_retrieval._clean_images()
