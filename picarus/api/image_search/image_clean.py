#!/usr/bin/env python
import hadoopy
import imfeat
import os
import hadoopy_hbase


class HBaseMapper(object):

    def __init__(self):
        super(HBaseMapper, self).__init__()
        self._hbase_input_column = os.environ['HBASE_INPUT_COLUMN'].split(':')
        self._hbase_output_column = os.environ['HBASE_OUTPUT_COLUMN'].split(':')
        self._hbase = hadoopy_hbase.HBaseRowDict(os.environ['HBASE_TABLE'], os.environ['HBASE_OUTPUT_COLUMN'])

    def map(self, row, columns):
        try:
            columns[self._hbase_output_column[0]][self._hbase_output_column[1]]
            hadoopy.counter('INPUT', 'Existing')
        except KeyError:
            for row, out in self._map(row, columns[self._hbase_input_column[0]][self._hbase_input_column[1]]):
                self._hbase[row] = out
            hadoopy.counter('INPUT', 'New')


class Mapper(HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()

    def _map(self, row, image_binary):
        try:
            image = imfeat.image_fromstring(image_binary)
            yield row, imfeat.image_tostring(imfeat.resize_image_max_side(image, 320), 'jpg')
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_INPUT_COLUMN', 'HBASE_TABLE', 'HBASE_OUTPUT_COLUMN'])
