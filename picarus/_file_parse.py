import gzip
import bz2
import json
import cPickle as pickle
import os


def _getext(fn):
    return fn.rsplit('/', 1)[-1].split('.', 1)[-1]


def load(fn):
    if not os.path.exists(fn):
        raise IOError('Path does not exist [%s]' % fn)
    try:
        ext = _getext(fn)
    except ValueError:
        raise ValueError('File needs an extension')
    if ext[-3:] == '.gz':
        fp = gzip.GzipFile(fn)
        ext = ext[:-3]
    elif ext[-4:] == '.bz2':
        fp = bz2.BZ2File(fn)
        ext = ext[:-4]
    else:
        fp = open(fn)
    if ext == 'js':
        return json.load(fp)
    elif ext == 'pkl':
        return pickle.load(fp)
    else:
        raise ValueError('File [%s] has unknown extension [%s]' % (fn, ext))


def dump(obj, fn):
    try:
        ext = _getext(fn)
    except ValueError:
        raise ValueError('File needs an extension')
    if ext[-3:] == '.gz':
        fp = gzip.GzipFile(fn, 'w')
        ext = ext[:-3]
    elif ext[-4:] == '.bz2':
        fp = bz2.BZ2File(fn, 'w')
        ext = ext[:-4]
    else:
        fp = open(fn, 'w')
    if ext == 'js':
        return json.dump(obj, fp)
    elif ext == 'pkl':
        return pickle.dump(obj, fp, -1)
    else:
        raise ValueError('File [%s] has unknown extension [%s]' % (fn, ext))
