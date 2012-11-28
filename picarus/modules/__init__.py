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
    - Simple, non-parametric

    Cons
    - Requires NN lookup for # descriptors * # classes which can be slow
    """
    def __init__(self, sbin=32, max_side=320, num_points=None, scale=1, required_files=()):
        self.required_files = required_files
        self.max_side = max_side
        self._feature = self._feature_hog_loc  # self._feature_hist
        self.db = None
        self.scale = scale
        self.num_points = num_points
        self.classes = None
        self.dist = distpy.L2Sqr()
        self.sbin = sbin

    def _feature_hog_loc(self, image):
        feature_mask = imfeat.HOGLatent(self.sbin).compute_dense_2d(image)
        features = []
        norm = np.asfarray(feature_mask.shape[:2])
        for y in range(feature_mask.shape[0]):
            for x in range(feature_mask.shape[1]):
                yx = np.array([y, x]) / norm * self.scale
                features.append(np.hstack([feature_mask[y, x, :], yx]))
        return np.asfarray(features)

    def _feature_hist(self, image):
        out = []
        for block in imfeat.BlockGenerator(image, imfeat.CoordGeneratorRect, output_size=(self.sbin, self.sbin), step_delta=(self.sbin, self.sbin)):
            out.append(imfeat.convert_image(image, {'type': 'numpy', 'dtype': 'float32', 'mode': 'lab'}).ravel())
        return np.asfarray(out)


    def feature(self, image):
        points = self._feature(imfeat.resize_image_max_side(image, self.max_side))
        if self.num_points is not None:
            return np.ascontiguousarray(random.sample(points, min(self.num_points, len(points))))
        return points

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
            features = self.feature(image)
            self.db.setdefault(cur_class, []).append(features)
        for cur_class, features in self.db.items():
            self.db[cur_class] = np.vstack(self.db[cur_class])

    def analyze(self, image):
        """Image Classifier

        Args:
            image: numpy bgr array

        Return:
            List of {'name': name} in
            descending confidence order.
        """
        features = self.feature(image)
        class_dists = {}  # [class] = total_dist
        for cur_class in self.db:
            dist_indeces = self.dist.nns(self.db[cur_class], features)
            class_dists[cur_class] = np.sum(dist_indeces[:, 0])
        return [{'class': self.classes[x[0]], 'distance': x[1]} for x in sorted(class_dists.items(),
                                                                                key=lambda x: x[1])]


class LocalNBNNClassifier(NBNNClassifier):
    """Multi-class classifier using Local Naive Bayes Nearest Neighbor

    Pros
    - Simple, non-parametric
    - Faster than NBNN because it only looks at K neighbors (joint space for all classes)

    Cons
    - Requires K-NN lookup for # descriptors
    - Approximates NBNN
    """
    def __init__(self, k=10, *args, **kw):
        super(LocalNBNNClassifier, self).__init__(*args, **kw)
        self.k = k

    def train(self, class_images):
        self.classes = []
        self.class_nums = []
        class_to_num = {}
        self.db = []  # features
        # Compute features
        for cur_class, image in class_images:
            if cur_class not in class_to_num:
                class_to_num[cur_class] = len(class_to_num)
                self.classes.append(cur_class)
            features = self.feature(image)
            self.class_nums += [class_to_num[cur_class]] * len(features)
            self.db.append(features)
        self.db = np.vstack(self.db)
        self.class_nums = np.array(self.class_nums)

    def analyze(self, image):
        """Image Classifier

        Args:
            image: numpy bgr array

        Return:
            List of {'name': name} in
            descending confidence order.
        """
        features = self.feature(image)
        class_dists = {}  # [class] = total_dist
        for feature in features:
            dist_indeces = self.dist.knn(self.db, feature, self.k + 1)
            dist_b = dist_indeces[self.k, 0]
            class_min_dists = {}
            for dist, index in dist_indeces[:self.k, :]:
                cur_class = self.class_nums[index]
                class_min_dists[cur_class] = min(class_min_dists.get(cur_class, float('inf')), dist)
            for cur_class, dist_c in class_min_dists.items():
                try:
                    class_dists[cur_class] += dist_c - dist_b
                except KeyError:
                    class_dists[cur_class] = dist_c - dist_b
        return [{'class': self.classes[x[0]], 'distance': x[1]} for x in sorted(class_dists.items(),
                                                                                key=lambda x: x[1])]

if __name__ == '__main__':
    c0 = LocalNBNNClassifier(num_points=100)
    c1 = NBNNClassifier(num_points=100)
    for c in [c0, c1]:
        images = [cv2.imread('/home/brandyn/projects/imfeat/tests/test_images/lena.ppm'),
                  cv2.imread('/home/brandyn/projects/imfeat/tests/test_images/opp_color_circle.png')]
        c.train(zip(['lena', 'opp'], images))
        print c.db[0].shape
        print c.db[1].shape
        print(c.db)
        print c.analyze(images[0])
