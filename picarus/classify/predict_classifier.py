import hadoopy
import picarus._file_parse as file_parse
import os
import picarus._classifiers as classifiers
import picarus
import numpy as np


class Mapper(object):

    def __init__(self):
        self._classifiers = [(x, classifiers.loads(y))
                             for x, y in file_parse.load(os.environ['CLASSIFIERS_FN'])]

    def _predict(self, classifier, feature):
        val = classifier.decision_function(np.array([feature]))[0]
        if val >= 0:
            return [(float(np.abs(val)), 1)]
        return [(float(np.abs(val)), -1)]

    @picarus.valid_image_check
    def map(self, image_hash, feature):
        """

        Args:
            image_hash: Unique image string
            feature: Numpy image feature

        Yields:
            A tuple in the form of (image_hash, predictions)
            image_hash: String representing the classifier
            predictions: Dictionary with key as classifier_name and value as prediction output
        """
        yield image_hash, dict((classifier_name, self._predict(classifier, feature))
                               for classifier_name, classifier in self._classifiers)

if __name__ == '__main__':
    hadoopy.run(Mapper)
