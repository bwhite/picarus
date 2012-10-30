#!/usr/bin/env python
import hadoopy
import imfeat
import os
import sys
import numpy as np
import json
import zlib
import hadoopy_hbase
import cPickle as pickle
from picarus._importer import call_import


class HBaseMapper(object):

    def __init__(self):
        super(HBaseMapper, self).__init__()
        self._hbase_input_column = os.environ['HBASE_INPUT_COLUMN'].split(':')
        self._hbase = hadoopy_hbase.HBaseRowDict(os.environ['HBASE_TABLE'], os.environ['HBASE_OUTPUT_COLUMN'])

    def map(self, row, columns):
        for row, out in self._map(row, columns[self._hbase_input_column[0]][self._hbase_input_column[1]]):
            self._hbase[row] = out


class Mapper(HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._hasher = pickle.load(open(os.environ['HASHER_FN']))

    def _map(self, row, feature_binary):
        try:
            feature = np.fromstring(feature_binary, dtype=np.float64)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
        else:
            yield row, self._hasher(feature).tostring()


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_INPUT_COLUMN', 'HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'HASHER_FN'])
