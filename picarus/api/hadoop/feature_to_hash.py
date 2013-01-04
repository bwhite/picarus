#!/usr/bin/env python
import hadoopy
import os
import numpy as np
import picarus.api


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._hasher = picarus.api.model_fromfile(os.environ['HASHER_FN'])

    def _map(self, row, feature_binary):
        feature = picarus.api.np_fromstring(feature_binary)
        yield row, self._hasher(feature).tostring()


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'HASHER_FN'])
