#!/usr/bin/env python
import hadoopy
import numpy as np
import picarus.api
import json


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()

    def _map(self, row, masks_binary):
        masks = picarus.api.np_fromstring(masks_binary)
        ilp = np.sum(masks.reshape((-1, masks.shape[-1])), 0)
        ilp /= masks.shape[0] * masks.shape[1]
        yield row, json.dumps(ilp.tolist(), separators=(',', ':'))

if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN'])
