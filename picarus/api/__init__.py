import zmq
from _picarus_search_pb2 import SearchIndex, NDArray
import numpy as np
import zlib
import json
import tempfile
import cPickle as pickle
from picarus._importer import call_import


def _tempfile(self, data, suffix=''):
    fp = tempfile.NamedTemporaryFile(suffix=suffix)
    fp.write(data)
    fp.flush()
    return fp


def model_fromfile(path):
    if path.endswith('.js.gz'):
        return call_import(json.loads(zlib.decompress(open(path).read())))
    elif path.endswith('.pkl.gz'):
        return pickle.loads(zlib.decompress(open(path).read()))
    else:
        raise ValueError('Unknown model type[%s]' % path)


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
