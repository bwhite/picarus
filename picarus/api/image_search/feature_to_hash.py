#!/usr/bin/env python
import hadoopy
import os
import numpy as np
from hbase_mapper import HBaseMapper
import picarus.api


class Mapper(HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._hasher = picarus.api.model_fromfile(os.environ['HASHER_FN'])

    def _map(self, row, feature_binary):
        try:
            feature = picarus.api.np_fromstring(feature_binary)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
        else:
            yield row, self._hasher(feature).tostring()


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_INPUT_COLUMN', 'HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'HASHER_FN'])
