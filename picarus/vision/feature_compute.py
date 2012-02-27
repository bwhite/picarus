import hadoopy
import imfeat
import os
import sys
import numpy as np
import time
import picarus._features as features


def _parse_height_width():
    try:
        image_width = image_height = int(os.environ['IMAGE_LENGTH'])
    except KeyError:
        image_width = int(os.environ['IMAGE_WIDTH'])
        image_height = int(os.environ['IMAGE_HEIGHT'])
    return image_height, image_width


class Mapper(object):

    def __init__(self):
        self._feat = features.select_feature(os.environ['FEATURE'])
        self._image_height, self._image_width = _parse_height_width()
        self._total_time = 0.
        self._num_images = 0

    def map(self, name, image_data):
        try:
            image = imfeat.image_fromstring(image_data)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
            return
        try:
            image = imfeat.resize_image(image, self._image_height, self._image_width)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
        start_time = time.time()
        f = self._feat(image)
        self._total_time += time.time() - start_time
        self._num_images += 1
        yield name, f

    def close(self):
        print('Average Feature Time [%f]' % (self._total_time / self._num_images))
        

if __name__ == '__main__':
    hadoopy.run(Mapper)
