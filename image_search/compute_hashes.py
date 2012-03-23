import hadoopy
import numpy as np
import cPickle as pickle
import os


def compute_hash(feature, median_feature):
    bit_shape = feature.shape[0], int(np.ceil(feature.shape[1] / 8.))
    return np.packbits(np.array(feature > median_feature, dtype=np.uint8)).reshape(bit_shape)


class Mapper(object):

    def __init__(self):
        self.median_feature = pickle.load(open(os.environ.get('MEDIAN_FEATURE_FN', 'median.pkl')))

    def map(self, key, value):
        feature = value.reshape((1, value.size))
        yield key, compute_hash(feature, self.median_feature)

if __name__ == "__main__":
    hadoopy.run(Mapper)

