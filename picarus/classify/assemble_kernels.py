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
            key: 
            value: 

        Yields:
            A tuple in the form of (key, value)
            key: 
            value: 
        """
        kernel, row_num = key
        yield kernel, (row_num, value)


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
        g = None
        for row_num, row in values:
            if g is None:
                sys.stderr.write('Allocating G!\n')
                g = np.zeros((row.size, row.size))
                sys.stderr.write('G was allocated!\n')
            g[row_num, :] = row.ravel()
        sys.stderr.write('Coercing to string!\n')
        g = g.tostring()
        sys.stderr.write('Done Coercing to string!\n')
        sys.stderr.write('Compress to string!\n')
        g = snappy.compress(g)
        sys.stderr.write('Done Compress to string!\n')
        yield key, g

if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
