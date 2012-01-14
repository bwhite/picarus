import hadoopy
import numpy as np


def mapper(k, v):
    if isinstance(v, tuple):  # (image_data, metadata)
        v = v[1]
    yield k, v


def reducer(k, vs):
    for v in vs:
        print(type(v))
        if isinstance(v, dict):
            metadata = v[1]
        else:
            feature_hash = v
    try:
        yield k, (feature_hash, metadata)
    except NameError:
        hadoopy.counter('ERRORS', 'JoinsFailed')
            

if __name__ == '__main__':
    hadoopy.run(mapper, reducer)
