#!/usr/bin/env python
import hadoopy
import imfeat
import os
import picarus.api


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self.max_side = int(os.environ.get['MAX_SIDE'])

    def _map(self, row, image_binary):
        try:
            image = imfeat.image_fromstring(image_binary)
            yield row, imfeat.image_tostring(imfeat.resize_image_max_side(image, self.max_side), 'jpg')
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_INPUT_COLUMN', 'HBASE_TABLE', 'HBASE_OUTPUT_COLUMN', 'MAX_SIDE'])
