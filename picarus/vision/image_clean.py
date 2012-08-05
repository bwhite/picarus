import hadoopy
import imfeat
import os
import numpy as np


class Mapper(object):

    def __init__(self):
        self.max_side = int(os.environ.get('MAX_SIDE'))
        self.filter_side = int(os.environ.get('FILTER_SIDE'))

    def map(self, name, image_data):
        try:
            image = imfeat.image_fromstring(image_data)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
            return
        if self.filter_side is not None and min(image.shape[0], image.shape[1]) < self.filter_side:
            hadoopy.counter('DATA_ERRORS', 'ImageTooSmallPre')
            return
        if self.max_side is not None:
            image = imfeat.resize_image_max_side(image, self.max_side)
        if self.filter_side is not None and min(image.shape[0], image.shape[1]) < self.filter_side:
            hadoopy.counter('DATA_ERRORS', 'ImageTooSmallPost')
            return
        yield name, imfeat.image_tostring(image, 'jpg')

if __name__ == '__main__':
    hadoopy.run(Mapper)
