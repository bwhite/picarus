import hadoopy
import numpy as np
import cPickle as pickle

class Mapper(object):

  def __init__(self):
      self.median_feature = pickle.load(open(os.environ.get('MEDIAN_FEATURE_FN', 'median.pkl')))

  def map(self, key, value):
      feature = value.reshape((1, value.size))
      bit_shape = feature.shape[0], int(np.ceil(feature.shape[1] / 8.))
      yield key, np.packbits(np.array(feature > self.median_feature, dtype=np.uint8)).reshape(bit_shape)

if __name__ == "__main__":
    hadoopy.run(Mapper)

