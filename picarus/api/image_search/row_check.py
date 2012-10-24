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
logging.basicConfig(level=logging.DEBUG)

a = hadoopy_hbase.connect()
for row, cols in hadoopy_hbase.scanner(a, 'sun397'):
    print(cols.keys())
    print imfeat.image_fromstring(cols['data:image']).shape
    print imfeat.image_fromstring(cols['data:image_clean']).shape
    print 'Hash Bits[%d]' % (np.fromstring(cols['data:hashes_gist'], dtype=np.uint8).size * 8,)
    print 'Feature Dims[%d]' % (np.fromstring(cols['data:feature_gist'], dtype=np.float64).size,)
    break
