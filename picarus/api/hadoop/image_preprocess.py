#!/usr/bin/env python
import hadoopy
import imfeat
import os
import picarus.api


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._preprocessor = picarus.api.model_fromfile(os.environ['MODEL_FN'])

    def _map(self, row, image_binary):
        yield row, self._preprocessor.asbinary(image_binary)

if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'MODEL_FN'])
