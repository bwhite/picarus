#!/usr/bin/env python
import hadoopy
import os
import numpy as np


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
            value: Any value (can't be of type dict) or predictions (of type dict)
        """
        yield image_hash, value


class Reducer(object):

    def __init__(self):
        self._class_name = os.environ['CLASSIFIER_NAME']
        self._class_thresh = float(os.environ['CLASSIFIER_THRESH'])
        self._output_class = int(os.environ['OUTPUT_CLASS'])

    def reduce(self, image_hash, values):
        """

        Args:
            image_hash: (see mapper)
            values: Iterator of values (see mapper)

        Yields:
            A tuple in the form of (image_hash, value)
            image_hash: Image hash
            value: The provided value (not the prediction)
        """
        predictions = None
        out_val = None
        for value in values:
            if isinstance(value, dict):
                predictions = value
            else:
                out_val = value
        if predictions is None or out_val is None:
            hadoopy.counter('DATA_ERR', 'MISSING_PREDICTIONS_OR_DATA')
            return
        label, conf = predictions[self._class_name][0]
        if (self._class_thresh <= label * conf) == (self._output_class == 1):  # Both true or both false
            yield image_hash, out_val


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
