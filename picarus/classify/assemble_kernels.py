import hadoopy
import sys
import numpy as np
import snappy


class Mapper(object):

    def __init__(self):
        pass

    def map(self, key, value):
        """

        Args:
            key: (kernel, row_num, col_num)
            value: value

        Yields:
            A tuple in the form of (key, value)
            key: (kernel, row_num)
            value: (col_num, value)
        """
        kernel, row_num, col_num = key
        yield (kernel, row_num), (col_num, value)


class Reducer(object):

    def __init__(self):
        pass

    def reduce(self, key, values):
        """

        Args:
            key: (see mapper)
            values: Iterator of values (see mapper)

        Yields:
            A tuple in the form of (key, value)
            key: 
            value: 
        """
        yield key, np.hstack([y[1] for y in sorted(values, key=lambda x: x[0])])

if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
