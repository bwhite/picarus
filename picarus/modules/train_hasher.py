import hadoopy
import os
import random
import image_search


# TODO: Put this mapper in Hadoopy helper
class Mapper(object):

    def __init__(self):
        self.kv_prob = float(os.environ['KV_PROB'])

    def map(self, k, v):
        if random.random() < self.kv_prob:
            yield 0, (k, v)


class Reducer(object):

    def __init__(self):
        self.hash_bits = int(os.environ['HASH_BITS'])

    def reduce(self, key, id_feats):
        yield key, image_search.RRMedianHasher(self.hash_bits, normalize_features=False).train([x for _, x in id_feats])

if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer, required_cmdenvs=['KV_PROB', 'HASH_BITS'])
