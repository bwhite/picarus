#!/usr/bin/env python
import hadoopy
import picarus_takeout
import os
import picarus.api
import zlib


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._model = zlib.decompress(open(os.environ['MODEL_FN']).read())
        print(self._model)
        self.job = picarus_takeout.ModelChain(self._model)

    def _map(self, row, input_binary):
        #try:
        yield row, self.job.process_binary(input_binary)
        #except:
        #    hadoopy.counter('ERROR', 'BadRow')
        #    print('Error on row[%r]' % row)

if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'MODEL_FN'])
