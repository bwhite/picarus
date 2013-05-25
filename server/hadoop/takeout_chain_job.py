#!/usr/bin/env python
import hadoopy
import picarus_takeout
import os
import picarus
import zlib
import sys


class Mapper(picarus.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self._model = zlib.decompress(open(os.environ['MODEL_FN']).read())
        self.job = picarus_takeout.ModelChain(self._model)

    def _map(self, row, input_binary):
        try:
            yield row, self.job.process_binary(input_binary)
        except:
            sys.stdout.flush()
            hadoopy.counter('STATUS', 'badRow')
        else:
            sys.stdout.flush()
            hadoopy.counter('STATUS', 'goodRow')

if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'MODEL_FN'])
