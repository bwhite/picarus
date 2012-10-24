import hadoopy
import numpy as np
import cPickle as pickle
import image_search


class Mapper(object):

    def __init__(self):
        self.hasher = pickle.load(open('hasher.pkl'))

    def map(self, name, feature):
        yield 0, (name, self.hasher(feature)[0])


class Reducer(object):

    def __init__(self):
        pass

    def reduce(self, key, name_hashes):
        names, hashes = zip(*name_hashes)
        yield np.array(names), np.ascontiguousarray(hashes)

if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer, required_files=['hasher.pkl'])
