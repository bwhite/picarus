import hadoopy
import file_parse
import os
import classifiers


class Mapper(object):

    def __init__(self):
        self._classifiers = [(x, classifiers.loads(y))
                             for x, y in file_parse.load(os.environ['CLASSIFIERS_FN'])]

    def map(self, image_hash, feature):
        """

        Args:
            image_hash: Unique image string
            feature: Numpy image feature

        Yields:
            A tuple in the form of (classifier_name, label_value)
            classifier_name: String representing the classifier
            label_value: (label, feature) where label is an int
        """
        yield image_hash, dict((classifier_name, classifier.predict(feature))
                               for classifier_name, classifier in self._classifiers)

if __name__ == '__main__':
    hadoopy.run(Mapper)
