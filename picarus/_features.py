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


def _object_bank():
    return imfeat.ObjectBank()


def _meta_hog_gradient():
    return imfeat.MetaFeature(imfeat.HOGLatent(), imfeat.GradientHistogram())


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


def _bovw_hog():
    hog = imfeat.HOGLatent(8, 2)
    clusters = pickle.load(open('hog_8_2_clusters.pkl'))
    return imfeat.BoVW(lambda x: hog.make_bow_mask(x, clusters), clusters.shape[0], 3)


def select_feature(feat_name):
    return {'gist': _gist, 'hist_joint': _hist_joint, 'eigenface': _eigenface,
            'hog': _hog, 'autocorrelogram': _autocorrelogram,
            'spatial_hist_joint': _spatial_hist_joint,
            'meta_gist_spatial_hist': _meta_gist_spatial_hist,
            'meta_gist_spatial_hist_autocorrelogram': _meta_gist_spatial_hist_autocorrelogram,
            'meta_hog_gist_hist': _meta_hog_gist_hist,
            'meta_hog_gradient': _meta_hog_gradient,
            'object_bank': _object_bank,
            'bovw_hog': _bovw_hog}[feat_name]()


def _dense_surf():
    import impoint
    s = impoint.SURF()
    return s.compute_dense
    

def select_feature_point(feat_name):
    return {'surf_dense': _dense_surf}[feat_name]()
