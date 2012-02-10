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
            A tuple in the form of ()

        """
        for class_name, prediction in predictions.items():
            yield class_name, (image_hash, prediction)


class Reducer(object):

    def __init__(self):
        self.sorted_image_hashes = None
    
    def reduce(self, class_name, image_hash_predictions):
        sorted_image_hashes, predictions = zip(*sorted(image_hash_predictions))
        if self.sorted_image_hashes is None:
            self.sorted_image_hashes = sorted_image_hashes
        else:
            assert self.sorted_image_hashes == sorted_image_hashes
        yield class_name, predictions

    def close(self):
        if self.sorted_image_hashes is not None:
            yield '', self.sorted_image_hashes

if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
