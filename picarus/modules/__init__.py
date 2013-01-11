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
import impoint
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


class ImageBlocks(object):

    def __init__(self, sbin, mode, num_sizes, num_points=None):
        self.sbin = sbin
        self.mode = mode
        self.num_sizes = num_sizes
        self.num_points = num_points

    def _feature(self, image):
        out = []
        for block, coords in imfeat.BlockGenerator(image, imfeat.CoordGeneratorRect, output_size=(self.sbin, self.sbin), step_delta=(self.sbin, self.sbin)):
            out.append(imfeat.convert_image(block, {'type': 'numpy', 'dtype': 'float32', 'mode': self.mode}).ravel())
        return np.asfarray(out)

    def compute_dense(self, image):
        points = []
        max_side = np.max(image.shape[:2])
        for x in range(self.num_sizes):
            if max_side <= 0:
                break
            image = imfeat.resize_image_max_side(image, max_side)
            cur_points = self._feature(image)
            if cur_points.size:
                points.append(cur_points)
            max_side = int(max_side / 2)
        if points:
            points = np.vstack(points)
        else:
            points = np.array([])
        if self.num_points is not None:
            points = random.sample(points, min(self.num_points, len(points)))
        points = np.ascontiguousarray(points)
        print(points.shape)
        return points


class SURF(object):

    def __init__(self, num_points=1000, max_points=10000):
        super(SURF, self).__init__()
        self.max_points = max_points  # max points computed internally
        self.num_points = num_points  # max points returned (randomly sampled from internal)
        self._args = (num_points, max_points)
        self._surf = impoint.SURF(max_points=max_points)

    def __reduce__(self):
        return (SURF, self._args)

    def compute_dense(self, image):
        points = [x['descriptor'] for x in self._surf(image)]
        points = random.sample(points, min(len(points), self.num_points))
        return np.ascontiguousarray(points, dtype=np.double)


class NBNNClassifier(MultiClassClassifier):
    """Multi-class classifier using Naive Bayes Nearest Neighbor

    Pros
    - Simple, non-parametric

    Cons
    - Requires NN lookup for # descriptors * # classes which can be slow
    """
    def __init__(self):
        self.db = None
        self.classes = None
        self.dist = distpy.L2Sqr()

    def train(self, label_values):
        self.classes = []
        class_to_num = {}
        self.db = {}  # [class] = features
        # Compute features
        for cur_class, features in label_values:
            if cur_class not in class_to_num:
                class_to_num[cur_class] = len(class_to_num)
                self.classes.append(cur_class)
            cur_class = class_to_num[cur_class]
            if features.ndim == 1:
                print('Skipping due to no features')
                continue
            self.db.setdefault(cur_class, []).append(features)
        for cur_class, features in self.db.items():
            self.db[cur_class] = np.vstack(self.db[cur_class])

    def __call__(self, value):
        class_dists = {}  # [class] = total_dist
        for cur_class in self.db:
            dist_indeces = self.dist.nns(self.db[cur_class], value)
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

    def train(self, label_values):
        self.classes = []
        self.class_nums = []
        class_to_num = {}
        self.db = []  # features
        # Compute features
        for cur_class, features in label_values:
            if cur_class not in class_to_num:
                class_to_num[cur_class] = len(class_to_num)
                self.classes.append(cur_class)
            if features.ndim == 1:
                print('Skipping due to no features')
                continue
            self.class_nums += [class_to_num[cur_class]] * len(features)
            self.db.append(features)
        self.db = np.vstack(self.db)
        self.class_nums = np.array(self.class_nums)

    def __call__(self, value):
        class_dists = {}  # [class] = total_dist
        for feature in value:
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


def logo_demo():
    feat = ImageBlocks(sbin=16, mode='lab', num_sizes=3, num_points=None)
    c0 = LocalNBNNClassifier()
    preprocessor = imfeat.ImagePreprocessor(method='max_side', size=80, compression='jpg')

    def get_data(path):
        for x in glob.glob(path + '/*'):
            entity = os.path.basename(x)
            for y in glob.glob(x + '/*'):
                fn = os.path.basename(y)
                print(y)
                try:
                    yield entity, preprocessor.asarray(open(y).read()).copy()
                except Exception, e:
                    print(e)
                    continue
    label_values = ((x, feat.compute_dense(y)) for x, y in get_data('/mnt/brandyn_extra/goodlogo_entity_images'))
    c0.train(label_values)
    total = 0
    good_10 = 0
    good_5 = 0
    good_1 = 0
    for entity, image in get_data('/home/brandyn/google_image_logos'):
        out = c0(feat.compute_dense(image))
        total += 1
        if entity in [x['class'] for x in out]:
            good_10 += 1
        if entity in [x['class'] for x in out[:5]]:
            good_5 += 1
        if entity in [x['class'] for x in out[:1]]:
            good_1 += 1
        print 10, good_10 / float(total)
        print 5, good_5 / float(total)
        print 1, good_1 / float(total)


def lena_demo():
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


if __name__ == '__main__':
    logo_demo()
