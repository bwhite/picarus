import hadoopy
import imfeat
import numpy as np



class Mapper(object):

  def __init__(self):
      pass

  def load_data(self, image_data, image_metadata):
      image_metadata['tags'] = image_metadata['tags'].split()
      image = imfeat.image_fromstring(image_data, {'type': 'numpy', 'dtype': 'uint8', 'mode': 'bgr'})
      return image, image_metadata

  def compute_feature(self, image):
      feature = imfeat.Histogram('lab', num_bins=8)
      return feature(imfeat.resize_image(image, 256, 256))

  def map(self, key, value):
      image_data, image_metadata = value
      image, image_metadata = self.load_data(image_data, image_metadata)
      feature = self.compute_feature(image)
      yield key, feature


if __name__ == "__main__":
    hadoopy.run(mapper)

