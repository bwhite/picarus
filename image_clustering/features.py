import imfeat
import face_feature
import cPickle as pickle
import numpy as np


def _hist_joint():
    return imfeat.Histogram('rgb', style='joint')


def _gist():
    return imfeat.GIST()


def _eigenface():
    return pickle.load(open('eigenfaces_lfw_cropped.pkl'))


def select_feature(feat_name):
    return {'gist': _gist, 'hist_joint': _hist_joint, 'eigenface': _eigenface}[feat_name]()
