import zmq
from _picarus_search_pb2 import SearchIndex, NDArray, Classifier
import numpy as np
import zlib
import json
import tempfile
import cPickle as pickle
import os
import hadoopy_hbase
from picarus._importer import call_import


def _tempfile(data, suffix=''):
    fp = tempfile.NamedTemporaryFile(suffix=suffix)
    fp.write(data)
    fp.flush()
    return fp


class HBaseMapper(object):

    def __init__(self):
        super(HBaseMapper, self).__init__()
        self._hbase_input_column = os.environ['HBASE_INPUT_COLUMN'].split(':')
        self._hbase = hadoopy_hbase.HBaseRowDict(os.environ['HBASE_TABLE'], os.environ['HBASE_OUTPUT_COLUMN'])

    def map(self, row, columns):
        for row, out in self._map(row, columns[self._hbase_input_column[0]][self._hbase_input_column[1]]):
            self._hbase[row] = out


def model_fromfile(path):
    if path.endswith('.js.gz'):
        return call_import(json.loads(zlib.decompress(open(path).read())))
    elif path.endswith('.pkl.gz'):
        return pickle.loads(zlib.decompress(open(path).read()))
    else:
        raise ValueError('Unknown model type[%s]' % path)


def classifier_fromstring(classifier_ser):
    cp = Classifier()
    cp.ParseFromString(classifier_ser)
    loader = lambda x, y: pickle.loads(y) if x == cp.PICKLE else call_import(json.loads(y))
    feature = loader(cp.feature_format, cp.feature)
    classifier = loader(cp.classifier_format, cp.classifier)
    return lambda image: int(classifier.predict(feature(image)).flat[0])


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
