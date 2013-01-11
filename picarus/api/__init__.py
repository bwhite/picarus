import zmq
from _picarus_search_pb2 import SearchIndex, NDArray, Classifier
import numpy as np
import zlib
import json
import tempfile
import cPickle as pickle
import os
import hadoopy_hbase
import base64
import imfeat
from picarus._importer import call_import


def _tempfile(data, suffix=''):
    fp = tempfile.NamedTemporaryFile(suffix=suffix)
    fp.write(data)
    fp.flush()
    return fp


class HBaseMapper(object):

    def __init__(self):
        super(HBaseMapper, self).__init__()
        self._hbase = hadoopy_hbase.HBaseRowDict(os.environ['HBASE_TABLE'], base64.b64decode(os.environ['HBASE_OUTPUT_COLUMN']))

    def map(self, row, value):
        for row, out in self._map(row, value):
            self._hbase[row] = out


def model_fromfile(path):
    if path.endswith('.js.gz'):
        return call_import(json.loads(zlib.decompress(open(path).read())))
    elif path.endswith('.pkl.gz'):
        return pickle.loads(zlib.decompress(open(path).read()))
    else:
        raise ValueError('Unknown model type[%s]' % path)


def _classifier_frompb(c, feature_input=False):
    loader = lambda x, y: pickle.loads(y) if x == c.PICKLE else call_import(json.loads(y))
    preprocessor = loader(c.preprocessor_format, c.preprocessor)
    feature = loader(c.feature_format, c.feature)
    classifier = loader(c.classifier_format, c.classifier)
    if c.classifier_type == c.CLASS_DISTANCE_LIST:
        classifier_func = classifier
    else:
        classifier_func = lambda feature: float(classifier.decision_function(feature).flat[0])
    if c.feature_type == c.FEATURE:
        feature_func = feature
    elif c.feature_type == c.MULTI_FEATURE:
        feature_func = lambda image: feature.compute_dense(image)
    else:
        raise ValueError('Unknown feature type')
    if feature_input:
        return classifier_func
    else:
        return lambda image: classifier_func(feature_func(preprocessor.asarray(image)))


def image_classifier_frompb(c):
    return _classifier_frompb(c)


def feature_classifier_frompb(c):
    return _classifier_frompb(c, feature_input=True)


def image_classifier_fromstring(c_ser):
    c = Classifier()
    c.ParseFromString(c_ser)
    return image_classifier_frompb(c)


def feature_classifier_fromstring(c_ser):
    c = Classifier()
    c.ParseFromString(c_ser)
    return feature_classifier_frompb(c)


def model_tofile(model):
    if isinstance(model, dict):
        return _tempfile(zlib.compress(json.dumps(model)), suffix='.js.gz')
    else:
        return _tempfile(zlib.compress(pickle.dumps(model)), suffix='.pkl.gz')


def np_tostring(array):
    array = np.ascontiguousarray(array)
    nda = NDArray()
    nda.data = array.tostring()
    nda.shape.extend(list(array.shape))
    nda.dtype = array.dtype.name
    return nda.SerializeToString()


def np_fromstring(array_ser):
    nda = NDArray()
    nda.ParseFromString(array_ser)
    return np.fromstring(nda.data, dtype=nda.dtype).reshape(nda.shape)
