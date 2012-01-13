import hadoopy
import numpy as np

class Mapper(object):
  def __init_(self):
    # TODO: load the median feature here
    # self.median_feature = ...
    pass
  
  def map(self, key, value):
    feature = value.reshape((1, value.size))
    bit_shape = (feature.shape[0], int(np.ceil(feature.shape[1] / 8.)))
    return np.packbits(np.array(feature > self.median_feature, dtype=np.uint8)).reshape(bit_shape)

if __name__ == "__main__":
  hadoopy.run(Mapper)

