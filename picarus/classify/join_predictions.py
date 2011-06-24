import hadoopy


class Mapper(object):

    def __init__(self):
        pass

    def map(self, image_hash, value):
        """

        Args:
            image_hash: Image hash
            value: Any value

        Yields:
            A tuple in the form of (image_hash, value)
            image_hash: Image hash
            value: Any value
        """
        yield image_hash, value


class Reducer(object):

    def __init__(self):
        pass

    def reduce(self, image_hash, values):
        """

        Args:
            image_hash: (see mapper)
            values: Iterator of values (see mapper)

        Yields:
            A tuple in the form of (image_hash, value)
            image_hash: Image hash
            value: (predictions, image_data)
        """
        predictions = None
        image_data = None
        for value in values:
            if isinstance(value, str):
                image_data = value
            else:
                predictions = value
        if not predictions or not image_data:
            hadoopy.counter('DATA_ERR', 'MISSING_PREDICTIONS_OR_DATA')
            return
        yield image_hash, (predictions, image_data)


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
