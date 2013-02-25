import imfeat
import picarus.vision.face_feature
import cPickle as pickle
import numpy as np
import bisect
import logging


class TextonPredict(imfeat.TextonBase):

    def __init__(self, *args, **kw):
        super(TextonPredict, self).__init__(*args, **kw)

    def __reduce__(self):
        return (TextonPredict, super(TextonPredict, self).__reduce__()[1])

    def __call__(self, *args, **kw):
        return self._predict(*args, **kw)[5]


class TextonILPPredict(object):

    def __init__(self, num_classes, ilp, forests, threshs):
        """
        Args:
            num_classes:
            ilp: Classifier used as the ILP
            forests: List of {'tp', 'tp2'}
            threshs: List of size len(forests) - 1
        """
        super(TextonILPPredict, self).__init__()
        self._reduce_args = (num_classes, ilp, forests, threshs)
        self.forests = [imfeat.TextonBase(num_classes=num_classes, **x) for x in forests]
        self.threshs = threshs
        self.ilp = picarus.api.image_classifier_fromstring(ilp)

    def __reduce__(self):
        return (TextonILPPredict, self._reduce_args)

    def __call__(self, image):
        conf = self.ilp(image)
        logging.debug('TextonILP[%f]' % conf)
        forest = self.forests[bisect.bisect_left(self.threshs, conf)]
        return forest._predict(image)[5]


class HOGBoVW(object):

    def __init__(self, clusters=None, levels=3, *args, **kw):
        super(HOGBoVW, self).__init__()
        self.hog = imfeat.HOGLatent(*args, **kw)
        self.levels = levels
        self.clusters = clusters
            
    @property
    def clusters(self):
        return self._clusters

    def _make_bow_mask(self, image):
        return self.hog.make_bow_mask(image, self._clusters)

    @clusters.setter
    def clusters(self, clusters):
        if clusters is None:
            self._clusters = None
            self._features = None
        else:
            clusters = np.asfarray(clusters)
            self._clusters = clusters
            self._feature = imfeat.BoVW(self._make_bow_mask,
                                        self._clusters.shape[0], self.levels)

    def cluster(self, features, num_clusters):
        import scipy.cluster.vq
        self.clusters = scipy.cluster.vq.kmeans(features, num_clusters)[0]

    def __call__(self, image):
        if self._feature is None:
            raise ValueError('Clusters not provided')
        return self._feature(image)
