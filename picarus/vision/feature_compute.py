import hadoopy
import imfeat
import os
import sys
import numpy as np
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
        #try:
        yield name, self._feat(image)
        #except Exception, e:
        #    hadoopy.counter('DATA_ERRORS', 'UnkImageType')
        #    print(str(e) + '\n')
        #    return


if __name__ == '__main__':
    hadoopy.run(Mapper)
