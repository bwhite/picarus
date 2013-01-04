import hadoopy
import hadoopy_hbase
import os
import image_search
import numpy as np
import cPickle as pickle
import picarus.api


class Mapper(object):

    def __init__(self):
        self._hbase_output_row = os.environ['HBASE_OUTPUT_ROW']

    def map(self, row, value):
        yield self._hbase_output_row, value


class Reducer(object):

    def __init__(self):
        self.hash_bits = int(os.environ['HASH_BITS'])
        self._hbase = hadoopy_hbase.HBaseRowDict(os.environ['HBASE_OUTPUT_TABLE'], os.environ['HBASE_OUTPUT_COLUMN'])

    def reduce(self, row, features):
        self._hbase[row] = pickle.dumps(image_search.RRMedianHasher(self.hash_bits, normalize_features=False).train([picarus.api.np_fromstring(x) for x in features]), -1)

if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer, required_cmdenvs=['HASH_BITS', 'HBASE_OUTPUT_ROW', 'HBASE_OUTPUT_TABLE', 'HBASE_OUTPUT_COLUMN'])
