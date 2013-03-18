#!/usr/bin/env python
import hadoopy
import os
import numpy as np
import json
import picarus.api
import picarus_takeout


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        classifier = picarus.api.model_fromfile(os.environ['CLASSIFIER_FN'])
        if os.environ['CLASSIFIER_TYPE'] == 'sklearn_decision_func':
            self._classifier = lambda x: repr(float(classifier.decision_function(x).flat[0]))
        elif os.environ['CLASSIFIER_TYPE'] == 'class_distance_list':
            self._classifier = lambda x: json.dumps(classifier(x))
        else:
            raise ValueError('Unknown CLASSIFIER_TYPE=%s' % os.environ['CLASSIFIER_TYPE'])

    def _map(self, row, feature_binary):
        feature = picarus.api.np_fromstring(feature_binary)
        yield row, self._classifier(feature)


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'CLASSIFIER_FN'])
