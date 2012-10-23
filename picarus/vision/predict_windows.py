import hadoopy
import picarus._file_parse as file_parse
import os
import picarus._classifiers as classifiers
import imfeat
from PIL import Image
import cStringIO as StringIO
from picarus import _features as features
from feature_compute import _parse_height_width
import numpy as np


class Mapper(object):

    def __init__(self):
        self._classifiers = [(x, classifiers.loads(y))
                             for x, y in file_parse.load(os.environ['CLASSIFIERS_FN'])]
        self._feat = features.select_feature(os.environ['FEATURE'])
        self._image_height, self._image_width = _parse_height_width()

    def map(self, image_hash, image_data):
        """

        Args:
            image_hash: Unique image string
            image_data: Binary image data

        Yields:
            A tuple in the form of (classifier_name, label_value)
            classifier_name: String representing the classifier
            label_value: (label, feature) where label is an int
        """
        try:
            image = Image.open(StringIO.StringIO(image_data))
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
            return
        bgen = imfeat.BlockGenerator(image, imfeat.CoordGeneratorRectRotate,
                                     output_size=(self._image_height, self._image_width),
                                     step_delta=(self._image_height / 2, self._image_width / 2), angle_steps=1)
        for num, (image_out, sim) in enumerate(bgen):
            feature = np.asfarray(imfeat.compute(self._feat, image_out)[0])
            pred = dict((classifier_name, classifier.predict(feature))
                        for classifier_name, classifier in self._classifiers)
            if any(x for x in pred.values() if x[0][0] * x[0][1] > 0):  # At least 1 class needs to be > 0
                image_out_fp = StringIO.StringIO()
                imfeat.convert_image(image_out, ['RGB']).save(image_out_fp, 'JPEG')
                image_out_fp.seek(0)
                yield (image_hash, sim), (pred, image_out_fp.read())

if __name__ == '__main__':
    hadoopy.run(Mapper)
