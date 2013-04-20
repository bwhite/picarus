#!/usr/bin/env python
import hadoopy
import picarus_takeout
import imfeat
import os
import picarus.api


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._preprocessor = picarus.api.model_fromfile(os.environ['MODEL_FN'])

    def _map(self, row, image_binary):
        try:
            yield row, self._preprocessor.asbinary(image_binary)
        except:
            hadoopy.counter('ERROR', 'PREPROCESSOR')
            print('Error on row[%r]' % row)

if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'MODEL_FN'])
