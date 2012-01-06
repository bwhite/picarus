import hadoopy
import picarus._file_parse as file_parse
import os
import picarus._classifiers as classifiers


class Mapper(object):

    def __init__(self):
        labels = file_parse.load(os.environ['LOCAL_LABELS_FN'])
        self._hash_class_labels = self._invert_labels(labels)

    def _invert_labels(self, labels):
        inverted = {}
        for classifier_name in labels:
            for label, keys in labels[classifier_name]['labels'].items():
                label = int(label)
                for k in keys:
                    inverted.setdefault(k, []).append((classifier_name, label))
        return inverted

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
        try:
            class_labels = self._hash_class_labels[image_hash]
        except KeyError:
            hadoopy.counter('DATA_ERRORS', 'UNKNOWN_IMAGE_HASH')
            return
        for classifier_name, label in class_labels:
            yield classifier_name, (label, feature)


class Reducer(object):

    def __init__(self):
        self._labels = file_parse.load(os.environ['LOCAL_LABELS_FN'])

    def reduce(self, classifier_name, label_values):
        """

        Args:
            classifier_name: (see mapper)
            label_values: Iterator of label_values (see mapper)

        Yields:
            A tuple in the form of (key, value)
            classifier_name: (see mapper)
            classifier: Serialized classifier
        """
        print('Starting [%s]' % str(classifier_name))
        cur_labels = self._labels[classifier_name]
        classifier = classifiers.train(cur_labels['classifier'], cur_labels['classifier_extra'], label_values)
        classifier_ser = classifiers.dumps(cur_labels['classifier'], cur_labels['classifier_extra'], classifier)
        yield classifier_name, classifier_ser
        print('Ending [%s,%d]' % (str(classifier_name), len(classifier_ser)))


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
