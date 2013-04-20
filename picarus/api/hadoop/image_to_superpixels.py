#!/usr/bin/env python
import hadoopy
import imfeat
import json
import imseg
import picarus.api


class Mapper(picarus.api.HBaseMapper):

    def __init__(self):
        super(Mapper, self).__init__()
        self.sp = imseg.SuperPixels()

    def _map(self, row, image_binary):
        try:
            image = imfeat.image_fromstring(image_binary)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
        out = self.sp(image, 25)
        hulls = self.sp.label_image_to_contours(out, 1.)
        yield row, json.dumps(hulls, separators=(',', ':'))


if __name__ == '__main__':
    hadoopy.run(Mapper, required_cmdenvs=['HBASE_TABLE', 'HBASE_OUTPUT_COLUMN'])
