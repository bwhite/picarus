#!/usr/bin/env python
import hadoopy
import os
import numpy as np
import picarus.api


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._classifier = picarus.api.feature_classifier_fromstring(open(os.environ['CLASSIFIER_FN']).read())

    def _map(self, row, feature_binary):
        feature = picarus.api.np_fromstring(feature_binary)
        yield row, np.double(self._classifier(feature)).tostring()


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'CLASSIFIER_FN'])
