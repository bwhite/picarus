import hadoopy
import imfeat
import os


class Mapper(object):

    def __init__(self):
        self._max_side = os.environ.get('MAX_SIDE')

    def map(self, name, image_data):
        try:
            image = imfeat.image_fromstring(image_data)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
            return
        try:
            image = imfeat.resize_image_max_side(image, self.max_side)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageResizeError')
        yield name, imfeat.image_tostring(image, 'jpg')

if __name__ == '__main__':
    hadoopy.run(Mapper)
