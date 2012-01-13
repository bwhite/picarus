import hadoopy
import numpy as np


def mapper(key, value):
    return enumerate(value)


def reducer(key, values):
    yield key, np.median(np.fromiter(values, dtype=np.float64))

if __name__ == "__main__":
    hadoopy.run(mapper)

