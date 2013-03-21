#!/usr/bin/env python
import hadoopy
import imfeat
import picarus_takeout
import os
import picarus.api


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._feat = self._feat_orig = picarus.api.model_fromfile(os.environ['MODEL_FN'])

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
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'MODEL_FN'])
