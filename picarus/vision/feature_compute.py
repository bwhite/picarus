import hadoopy
import imfeat
import Image
import cStringIO as StringIO
import os
import numpy as np
import picarus._features as features


class Mapper(object):

    def __init__(self):
        self._feat = features.select_feature(os.environ['FEATURE'])
        self._image_length = int(os.environ['IMAGE_LENGTH'])

    def map(self, name, image_data):
        try:
            image = Image.open(StringIO.StringIO(image_data))
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
            return
        try:
            image = image.resize((self._image_length, self._image_length))
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
        try:
            yield name, np.asfarray(imfeat.compute(self._feat, image)[0])
        except ValueError, e:
            print(e)
            hadoopy.counter('DATA_ERRORS', 'UnkImageType')
            return


if __name__ == '__main__':
    hadoopy.run(Mapper)
