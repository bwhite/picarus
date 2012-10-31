import hadoopy_hbase
import logging
import time
import tempfile
import zlib
import json
import os
import random
import numpy as np
import imfeat
import picarus.modules
import picarus.api
logging.basicConfig(level=logging.DEBUG)

a = hadoopy_hbase.connect()
hrc = picarus.modules.HashRetrievalClassifier()
hrc.load(open('sun397_index.pb').read())
for row, cols in hadoopy_hbase.scanner(a, 'images'):
    image = imfeat.image_fromstring(cols['data:image'])
    print imfeat.image_fromstring(cols['data:image']).shape
    print imfeat.image_fromstring(cols['data:image_320']).shape
    print('image_75sq[%d]' % len(cols['data:image_75sq']))
    print row
    cur_f = np.fromstring(cols['feat:gist'], dtype=np.float64)
    cur_h = np.fromstring(cols['hash:gist'], dtype=np.uint8)
    print 'Hash Bits[%d]' % (cur_h.size * 8,)
    print 'Feature Dims[%d]' % (cur_f.size,)
    f = hrc.feature(image)
    h = hrc.hasher(f).ravel()
    print cur_f
    print f
    print cur_h
    print h
