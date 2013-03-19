#!/usr/bin/env python
import hadoopy
import imfeat
import picarus_takeout
import os
import picarus.api


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._feat = self._feat_orig = picarus.api.model_fromfile(os.environ['FEATURE_FN'])
        self._type = os.environ['FEATURE_TYPE']
        if self._type == 'multi_feature':
            self._feat = lambda x: self._feat_orig.compute_dense(x)

    def _map(self, row, image_binary):
        try:
            if not image_binary:
                raise ValueError
            image = imfeat.image_fromstring(image_binary)
        except:
            hadoopy.counter('ERROR', 'FEATURE')
            print('Error on row[%r]' % row)
        else:
            yield row, picarus.api.np_tostring(self._feat.compute_feature(image))


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'FEATURE_FN', 'FEATURE_TYPE'])
