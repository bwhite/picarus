import cPickle as pickle
import os
import cv2
import image_search
import numpy as np
import random
import glob
import picarus
import hadoopy
import hadoopy_helper
import imfeat
import vidfeat
from PIL import Image
import sklearn.svm
import picarus.api
import json
import distpy
from picarus._importer import call_import


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


class MultiClassClassifier(object):

    def __init__(self, required_files=()):
        self.required_files = required_files

    def imread(self, fn):
        out = cv2.imread(fn)
        if out is not None:
            return out
        return imfeat.convert_image(Image.open(fn), {'type': 'numpy', 'dtype': 'uint8', 'mode': 'bgr'})


class HashRetrievalClassifier(MultiClassClassifier):
    """Multi-class classifier implemented using linear SVMs, 1 positive per classifier

    Maintains a floating point matrix of C x F dims for C classifiers and F features,
    we compute the feature on the input image and then project it along the classifiers.

    Pros
    - Fast prediction compared to non-linear classifiers (prediction is done using BLAS in numpy)
    - Allows for instance specific feature weightings, this improves quality
    - As it is exemplar based, the classifier/example correspondence can be used for user feedback

    Cons
    - Large memory requirement per classifier compared to hashing
    - Quality not as good as non-linear classifiers
    """

    def __init__(self, required_files=()):
        self.required_files = required_files
        self.max_side = 320

    def _cluster_bovw(self, images, points_per_image=100, num_clusters=256):
        hog = imfeat.HOGLatent(8, 2)
        clusters = np.asfarray(imfeat.BoVW.cluster(images, hog.compute_dense, num_clusters, points_per_image))
        pickle.dump(clusters, open('hog_8_2_clusters.pkl', 'w'), -1)

    def load(self, proto_data, load_feature=True, load_hasher=True, load_index=True):
        si = picarus.api.SearchIndex()
        si.ParseFromString(proto_data)
        loader = lambda x, y: pickle.loads(y) if x == si.PICKLE else call_import(json.loads(y))
        self.metadata = np.array(si.metadata)
        if load_index:
            self.index = loader(si.index_format, si.index)
        if load_hasher:
            self.hasher = loader(si.hash_format, si.hash)
        if load_feature:
            f = loader(si.feature_format, si.feature)
            self.feature = lambda y: f(imfeat.resize_image_max_side(y, self.max_side))
        return self

    def train(self, images):
        self.hasher.train([self.feature(x) for x in images])

    def compute_db_hadoop(self, hdfs_path):
        import json
        si = picarus.api.SearchIndex()
        si.name = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        si.feature = json.dumps(self.feature_dict)  # TODO: What to do with the pkl file?
        with hadoopy_helper.hdfs_temp() as hdfs_output:
            picarus.vision.run_image_clean(hdfs_path, hdfs_output + '/clean', max_side=self.max_side)
            # Compute features (map)
            picarus.vision.run_image_feature(hdfs_output + '/clean', hdfs_output + '/feature', self.feature_dict, files=self.required_files)
            # Random sample features for hashes (map) and train hasher (reduce)
            hadoopy.launch_frozen(hdfs_output + '/feature', hdfs_output + '/hasher', _lf('train_hasher.py'), cmdenvs={'KV_PROB': 1.,
                                                                                                                      'HASH_BITS': 128})
            hasher = hadoopy.readtb(hdfs_output + '/hasher').next()[1]
            si.hash = pickle.dumps(hasher, -1)
            si.hash_format = si.PICKLE
            # Compute features hashes (map) and build database (reduce)
            open('hasher.pkl', 'w').write(si.hash)
            hadoopy.launch_frozen(hdfs_output + '/feature', hdfs_output + '/db', _lf('build_db.py'), files=['hasher.pkl'])
            metadata, hashes = hadoopy.readtb(hdfs_output + '/db').next()
            self.metadata = metadata
            si.metadata.extend(metadata.tolist())
            self.index = image_search.LinearHashDB().store_hashes(hashes, np.arange(len(metadata), dtype=np.uint64))
            si.index = pickle.dumps(self.index, -1)
            si.index_format = si.PICKLE
            open('index.pb', 'w').write(si.SerializeToString())

    def analyze_cropped(self, image, k=20):
        """Cropped Image Classifier

        Args:
            image: numpy bgr array

        Return:
            List of {'name': name} in
            descending confidence order.
        """
        feat = self.feature(image)
        h = self.hasher(feat).ravel()
        print('HashShape[%s]' % str(h.shape))
        entity_files = [json.loads(x) for x in self.metadata[self.index.search_hash_knn(h, k)].tolist()]
        return [{'entity': x, 'file': y} for x, y in entity_files]


class NBNNClassifier(MultiClassClassifier):
    """Multi-class classifier using Naive Bayes Nearest Neighbor


    Pros

    Cons
    """

    def __init__(self, required_files=()):
        self.required_files = required_files
        self.max_side = 320
        self.feature = imfeat.HOGLatent(32)
        self.db = None
        self.classes = None
        self.dist = distpy.L2Sqr()

    def train(self, class_images):
        self.classes = []
        class_to_num = {}
        self.db = {}  # [class] = features
        # Compute features
        for cur_class, image in class_images:
            if cur_class not in class_to_num:
                class_to_num[cur_class] = len(class_to_num)
                self.classes.append(cur_class)
            cur_class = class_to_num[cur_class]
            cur_features = self.feature.compute_dense(imfeat.resize_image_max_side(image, self.max_side))
            self.db.setdefault(cur_class, []).append(cur_features)
        for cur_class, features in self.db.items():
            self.db[cur_class] = np.vstack(self.db[cur_class])

    def analyze(self, image, k=1):
        """Image Classifier

        Args:
            image: numpy bgr array

        Return:
            List of {'name': name} in
            descending confidence order.
        """
        features = self.feature.compute_dense(imfeat.resize_image_max_side(image, self.max_side))
        class_dists = {}  # [class] = total_dist
        for cur_class in self.db:
            dist_indeces = self.dist.nns(self.db[cur_class], features)
            class_dists[cur_class] = np.sum(dist_indeces[:, 0])
            print(dist_indeces)
        print(class_dists)
        return [{'class': self.classes[x[0]]} for x in sorted(class_dists.items(),
                                                              key=lambda x: x[1])][:k]


if __name__ == '__main__':
    c = NBNNClassifier()
    images = [cv2.imread('/home/brandyn/projects/imfeat/tests/test_images/lena.ppm'),
              cv2.imread('/home/brandyn/projects/imfeat/tests/test_images/opp_color_circle.png')]
    c.train(images, ['lena', 'opp'])
    print c.db[0].shape
    print c.db[1].shape
    print(c.db)
    print c.analyze(images[0])
