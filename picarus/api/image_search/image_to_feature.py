#!/usr/bin/env python
import hadoopy
import imfeat
import os
import picarus.api


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._feat = picarus.api.model_fromfile(os.environ['FEATURE_FN'])

    def _map(self, row, image_binary):
        image = imfeat.image_fromstring(image_binary)
        yield row, picarus.api.np_tostring(self._feat(image))


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'FEATURE_FN'])
