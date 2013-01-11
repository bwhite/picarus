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
import time
logging.basicConfig(level=logging.DEBUG)

a = hadoopy_hbase.connect()
for row, cols in hadoopy_hbase.scanner(a, 'images', start_row='landmarks:flickr', stop_row='landmarks:flicks', columns=['meta:']):
    if cols['meta:class'] in ['food:flickr', 'white house']:
        a.deleteAllRow('images', row)
        print(cols)
    continue
    print(row)
    print(cols.keys())
    print('Fixing')
    ms = [hadoopy_hbase.Mutation(column='feat:hash_gist', isDelete=True),
          hadoopy_hbase.Mutation(column='hash:gist', value=cols['feat:hash_gist'])]
    a.mutateRow('sun397', row, ms)
    #print(row)
    #a.deleteAllRow('sun397', row)
    #del cols['data:hashes_gist']
    #row = os.path.basename(row)
    #cols['meta:file'] = row
    #row = json.dumps([cols['meta:class'], row], separators=(',', ':'))
    #ms = [hadoopy_hbase.Mutation(column=x, value=y) for x, y in cols.items()]
    #print(row)
    #print(cols.keys())
    #a.mutateRow('sun397', row, ms)
