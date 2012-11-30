import imfeat
import picarus.vision.face_feature
import cPickle as pickle
import numpy as np


def _hist_joint():
    return imfeat.Histogram('rgb', style='joint')


def _tiny_image():
    return imfeat.TinyImage()


def _lab_hist_joint_8bins():
    return imfeat.Histogram('lab', style='joint', num_bins=8)


def _lab_pyramid_4level_hist_4_11_11bins():
    return imfeat.PyramidHistogram('lab', levels=4, num_bins=[4, 11, 11])


def _spatial_hist_joint():
    return imfeat.SpatialHistogram(3, mode='hsv', style='joint')


def _spatial3_lab_hist_joint_4bins():
    return imfeat.SpatialHistogram(3, mode='lab', style='joint', num_bins=4)


def _gist():
    return imfeat.GIST()


def _hog():
    return imfeat.HOGLatent()


def _object_bank():
    return imfeat.ObjectBank()


def _gradient_hist():
    return imfeat.GradientHistogram()


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


def _bovw_hog(clusters=None):
    if clusters is None:
        clusters = pickle.load(open('hog_8_2_clusters.pkl'))
    clusters = np.asfarray(clusters)
    hog = imfeat.HOGLatent(8, 2)
    return imfeat.BoVW(lambda x: hog.make_bow_mask(x, clusters), clusters.shape[0], 3)


def _texton_4levels():
    return imfeat.TextonSpatialHistogram(levels=4)


def _texton_5levels_norm_thresh35pct():
    return imfeat.TextonSpatialHistogram(levels=5, norm=True, other_class_thresh=.35)


def select_feature(feat_name):
    f = {'gist': _gist, 'hist_joint': _hist_joint, 'eigenface': _eigenface,
         'hog': _hog,
         'autocorrelogram': _autocorrelogram,
         'spatial_hist_joint': _spatial_hist_joint,
         'meta_gist_spatial_hist': _meta_gist_spatial_hist,
         'meta_gist_spatial_hist_autocorrelogram': _meta_gist_spatial_hist_autocorrelogram,
         'meta_hog_gist_hist': _meta_hog_gist_hist,
         'meta_hog_gradient': _meta_hog_gradient,
         'object_bank': _object_bank,
         'bovw_hog': _bovw_hog,
         'spatial3_lab_hist_joint_4bins': _spatial3_lab_hist_joint_4bins,
         'lab_hist_joint_8bins': _lab_hist_joint_8bins,
         'gradient_hist': _gradient_hist,
         'tiny_image': _tiny_image,
         'texton_4levels': _texton_4levels,
         'texton_5levels_norm_thresh35pct': _texton_5levels_norm_thresh35pct,
         'lab_pyramid_4level_hist_4_11_11bins': _lab_pyramid_4level_hist_4_11_11bins}[feat_name]()

    def post_process(x):
        out = np.asfarray(f(x))
        return out
    return post_process


def _dense_surf():
    import impoint
    s = impoint.SURF()
    return s.compute_dense
    

def select_feature_point(feat_name):
    return {'surf_dense': _dense_surf}[feat_name]()


class TextonPredict(imfeat.TextonBase):

    def __init__(self, *args, **kw):
        super(TextonPredict, self).__init__(*args, **kw)

    def __reduce__(self):
        return (TextonPredict, super(TextonPredict, self).__reduce__()[1])

    def __call__(self, *args, **kw):
        return self._predict(*args, **kw)[5]


class HOGBoVW(object):

    def __init__(self, clusters=None, levels=3, *args, **kw):
        super(HOGBoVW, self).__init__()
        self.hog = imfeat.HOGLatent(*args, **kw)
        self.levels = levels
        self.clusters = clusters
            
    @property
    def clusters(self):
        return self._clusters

    @clusters.setter
    def _set_clusters(self, clusters):
        if clusters is None:
            self._clusters = None
            self._features = None
        else:
            self._clusters = clusters
            self._feature = imfeat.BoVW(lambda x: self.hog.make_bow_mask(x, self._clusters),
                                        self._clusters.shape[0], self.levels)

    def cluster(self, features, num_clusters):
        import scipy.cluster.vq
        self.clusters = scipy.cluster.vq.kmeans(features, num_clusters)[0]

    def __call__(self, image):
        if self._feature is None:
            raise ValueError('Clusters not provided')
        return self._feature(image)
    
