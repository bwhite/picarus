import hadoopy
import imfeat
import Image
import cStringIO as StringIO
import os
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
            image = Image.open(StringIO.StringIO(image_data))
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
            return
        try:
            image = image.resize((self._image_width, self._image_height))
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
        try:
            yield name, np.asfarray(imfeat.compute(self._feat, image)[0])
        except:
            hadoopy.counter('DATA_ERRORS', 'UnkImageType')
            return


if __name__ == '__main__':
    hadoopy.run(Mapper)
