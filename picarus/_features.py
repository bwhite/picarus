import imfeat
import picarus.vision.face_feature
import cPickle as pickle
import numpy as np


def _hist_joint():
    return imfeat.Histogram('rgb', style='joint')


def _spatial_hist_joint():
    return imfeat.SpatialHistogram(3, mode='hsv', style='joint')


def _gist():
    return imfeat.GIST()


def _hog():
    return imfeat.HOGLatent()


def _autocorrelogram():
    return imfeat.Autocorrelogram()


def _meta_gist_spatial_hist():
    return imfeat.MetaFeature(_gist(), _spatial_hist_joint())


def _meta_gist_spatial_hist_autocorrelogram():
    return imfeat.MetaFeature(_gist(), _spatial_hist_joint(), _autocorrelogram())


def _meta_hog_gist_hist():
    return imfeat.MetaFeature(_gist(), _hog(), _hist_joint())


def _eigenface():
    return pickle.load(open('eigenfaces_lfw_cropped.pkl'))


def select_feature(feat_name):
    return {'gist': _gist, 'hist_joint': _hist_joint, 'eigenface': _eigenface,
            'hog': _hog, 'autocorrelogram': _autocorrelogram,
            'spatial_hist_joint': _spatial_hist_joint,
            'meta_gist_spatial_hist': _meta_gist_spatial_hist,
            'meta_gist_spatial_hist_autocorrelogram': _meta_gist_spatial_hist_autocorrelogram,
            'meta_hog_gist_hist': _meta_hog_gist_hist}[feat_name]()
