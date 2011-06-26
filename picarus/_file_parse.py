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
    fn_orig = fn
    if fn.endswith('.gz'):
        fp = gzip.GzipFile(fn)
        fn = fn[:-3]
    elif fn.endswith('.bz2'):
        fp = bz2.BZ2File(fn)
        fn = fn[:-4]
    else:
        fp = open(fn)
    if fn.endswith('.js'):
        return json.load(fp)
    elif fn.endswith('.pkl'):
        return pickle.load(fp)
    else:
        raise ValueError('File [%s] has unknown extension' % fn_orig)


def dump(obj, fn):
    fn_orig = fn
    if fn.endswith('.gz'):
        fp = gzip.GzipFile(fn, 'w')
        fn = fn[:-3]
    elif fn.endswith('.bz2'):
        fp = bz2.BZ2File(fn, 'w')
        fn = fn[:-4]
    else:
        fp = open(fn, 'w')
    if fn.endswith('.js'):
        return json.dump(obj, fp)
    elif fn.endswith('.pkl'):
        return pickle.dump(obj, fp, -1)
    else:
        raise ValueError('File [%s] has unknown extension' % fn_orig)
