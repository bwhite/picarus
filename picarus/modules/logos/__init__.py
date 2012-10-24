import image_search
import imfeat
import picarus
import os
import cPickle as pickle
import numpy as np
import cv2


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


class LogoProcessor(picarus.modules.HashRetrievalClassifier):

    def __init__(self):
        super(LogoProcessor, self).__init__()
        self.max_side = 160
        self._feature_dict = None

    @property
    def feature_dict(self):
        if self._feature_dict is None:
            features = []
            features.append({'name': 'picarus._features._bovw_hog', 'kw': {'clusters': pickle.load(open('hog_8_2_clusters.pkl')).tolist()}})
            features.append({'name': 'imfeat.SpatialHistogram', 'args': [4, 4], 'kw': {'mode': 'lab', 'num_bins': 4}})
            self._feature_dict = {'name': 'imfeat.MetaFeature', 'args': features}
        return self._feature_dict

    @feature_dict.setter
    def feature_dict(self, value):
        self._feature_dict = value
