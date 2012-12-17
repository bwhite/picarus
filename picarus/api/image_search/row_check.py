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
hrc.load(open('sun397_feature_index.pb').read())
for num, (row, cols) in enumerate(hadoopy_hbase.scanner(a, 'images', start_row='sun397:train')):
    if num > 1:
        break
    for col in cols:
        if col.startswith('data:'):
            print repr(col), imfeat.image_fromstring(cols[col]).shape
        if col.startswith('feat:'):
            print repr(col), picarus.api.np_fromstring(cols[col]).shape
    print(cols.keys())
    continue
    print cols['feat:superpixel'][:50]
    image = imfeat.image_fromstring(cols['data:image_320'])
    print imfeat.image_fromstring(cols['data:image']).shape
    print imfeat.image_fromstring(cols['data:image_320']).shape
    print('image_75sq[%d]' % len(cols['data:image_75sq']))
    print row
    cur_f = picarus.api.np_fromstring(cols['feat:gist'])
    cur_h = np.fromstring(cols['hash:gist'], dtype=np.uint8)
    print 'HOG', picarus.api.np_fromstring(cols['feat:bovw_hog_levels2_sbin16_blocks1_clusters100'])
    print 'Hash Bits[%d]' % (cur_h.size * 8,)
    print 'Feature Dims[%d]' % (cur_f.size,)
    f = hrc.feature(image)
    h = hrc.hasher(f).ravel()
    #print cur_f
    #print f
    print cur_h
    print h

