import hadoopy
import numpy as np
import picarus


class Mapper(object):

    def __init__(self):
        pass

    @picarus.valid_image_check
    def map(self, image_hash, feature):
        """

        Args:
            image_hash: Unique image string
            feature: Numpy image feature

        Yields:
            A tuple in the form of (key, value)
            key: Either '0' or '1'
            value: feature or (image_hash, feature)
        """
        yield '0', feature
        yield '1', (image_hash, feature)


class Reducer(object):

    def __init__(self):
        pass

    def reduce(self, key, values):
        """

        Args:
            key: Either '0' or '1'
            value: feature or (image_hash, feature)

        Yields:
            A tuple in the form of (image_hash, feature)
            image_hash: Unique image string
            feature: Numpy image feature
        """
        if key == '0':
            c = s = ss = 0
            for i in values:
                c += 1
                s += i
                ss += i ** 2
            self.mean = s / c
            self.std = np.sqrt((ss - s ** 2 / c) / c)
        else:
            prev_err = np.seterr(all='ignore')
            for image_hash, feature in values:
                yield image_hash, np.nan_to_num((feature - self.mean) / self.std)
            np.seterr(**prev_err)

if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
