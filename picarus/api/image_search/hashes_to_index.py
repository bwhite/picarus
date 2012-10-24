import hadoopy
import hadoopy_hbase
import os
import image_search
import numpy as np
import cPickle as pickle
import picarus.api


class Mapper(object):

    def __init__(self):
        self._hbase_input_column = os.environ['HBASE_INPUT_COLUMN'].split(':')
        self._hbase_output_row = os.environ['HBASE_OUTPUT_ROW']

    def map(self, row, columns):
        yield self._hbase_output_row, (row, columns[self._hbase_input_column[0]][self._hbase_input_column[1]])


class Reducer(object):

    def __init__(self):
        self._hbase = hadoopy_hbase.HBaseRowDict(os.environ['HBASE_OUTPUT_TABLE'], os.environ['HBASE_OUTPUT_COLUMN'])

    def reduce(self, row, metadata_hashes):
        si = picarus.api.SearchIndex()
        si.ParseFromString(open(os.environ['INDEX_FN']).read())
        metadata, hashes = zip(*metadata_hashes)
        hashes = np.ascontiguousarray([np.fromstring(h, dtype=np.uint8) for h in hashes])
        si.metadata.extend(metadata)
        index = image_search.LinearHashDB().store_hashes(hashes, np.arange(len(metadata), dtype=np.uint64))
        si.index = pickle.dumps(index, -1)
        si.index_format = si.PICKLE
        self._hbase[row] = si.SerializeToString()

if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer, required_cmdenvs=['HBASE_INPUT_COLUMN', 'HBASE_OUTPUT_ROW', 'HBASE_OUTPUT_TABLE', 'HBASE_OUTPUT_COLUMN', 'INDEX_FN'])
