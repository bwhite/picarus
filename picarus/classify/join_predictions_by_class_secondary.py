import hadoopy


class Mapper(object):

    def __init__(self):
        pass

    def map(self, image_hash, predictions):
        """

        Args:
            image_hash: String representing the classifier
            predictions: Dictionary with key as classifier_name and value as prediction output

        Yields:
            A tuple in the form of (classifier_name, label_value)
            class_name_image_hash: String representing the class and image hash in the form of class_name\timage_hash
                a modified partitioner will be used to sort the image hashes as the enter the reducer.
            prediction: Classifier prediction
        """
        for class_name, prediction in predictions.items():
            yield '%s\t%s' % (class_name, image_hash), prediction


class Reducer(object):

    def __init__(self):
        self.cur_class_name = None
        self.cur_predictions = None
        self.sorted_image_hashes = []

    def reduce(self, class_name_image_hash, predictions):
        """
        Args:
            class_name_image_hash: String representing the class and image hash in the form of class_name\timage_hash
                a modified partitioner will be used to sort the image hashes as the enter the reducer.
            predictions: Iterator of one classifier prediction

        Yields:
            class_name: String class name
            predictions: List of classifier predictions

            or

            class_name: Empty string ''
            sorted_image_hashes: Sorted image hashes
        """
        print(class_name_image_hash)
        prediction, = list(predictions)  # NOTE(brandyn): This enforces that there is only one
        class_name, image_hash = class_name_image_hash.split('\t', 1)
        # Per class initial case
        if class_name != self.cur_class_name:
            for x in self.close(False):
                yield x
            self.cur_class_name = class_name
            self.cur_predictions = []
        # NOTE(brandyn): This can be removed after we are sure it is operating correctly
        if len(self.cur_predictions) == len(self.sorted_image_hashes):
            # If this is our first class, add the image hashes
            self.sorted_image_hashes.append(image_hash)
        else:
            # Check that image hashes are sorted correctly
            print(len(self.sorted_image_hashes))
            assert self.sorted_image_hashes[len(self.cur_predictions)] == image_hash
        self.cur_predictions.append(prediction)

    def close(self, done=True):
        if self.cur_class_name is not None:
            yield self.cur_class_name, self.cur_predictions
        if done:
            yield '', self.sorted_image_hashes

if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
