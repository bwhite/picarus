import hadoopy
import picarus._file_parse as file_parse
import os
import picarus._classifiers as classifiers


class Mapper(object):

    def __init__(self):
        self.labels = file_parse.load(os.environ['LOCAL_LABELS_FN'])

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
            label_classes = self.labels['inputs'][image_hash]['classes'].items()
        except KeyError:
            hadoopy.counter('DATA_ERRORS', 'UNKNOWN_IMAGE_HASH')
            return
        for label, class_names in label_classes:
            for class_name in class_names:
                yield class_name, (int(label), feature)


class Reducer(object):

    def __init__(self):
        self.labels = file_parse.load(os.environ['LOCAL_LABELS_FN'])

    def reduce(self, class_name, label_values):
        """

        Args:
            class_name: (see mapper)
            label_values: Iterator of label_values (see mapper)

        Yields:
            A tuple in the form of (key, value)
            classifier_name: (see mapper)
            classifier: Serialized classifier
        """
        label_values = list(label_values)
        for classifier_name in self.labels['classes'][class_name]['classifiers']:
            print('Starting [%s,%s]' % (class_name, classifier_name))
            classifier_extra = self.labels['classifiers'][classifier_name].get('extra', '')
            classifier = classifiers.train(self.labels['classifiers'][classifier_name]['name'], classifier_extra, label_values)
            classifier_ser = classifiers.dumps(classifier_name, classifier_extra, classifier)
            yield ' '.join([class_name, classifier_name]), classifier_ser
            print('Ending [%s,%s,%d]' % (class_name, classifier_name, len(classifier_ser)))


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
