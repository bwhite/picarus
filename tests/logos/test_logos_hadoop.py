import logging
import glob
import hadoopy
import os
import json
import cv2
import shutil
from picarus.modules.logos import LogoProcessor

logging.basicConfig(level=logging.DEBUG)
try:
    import unittest2 as unittest
except ImportError:
    import unittest


def compare_to_local(lp):
    path = '/home/brandyn/projects/crawlers/goodlogo/images'
    results_path = 'results'
    try:
        shutil.rmtree(results_path)
    except OSError:
        pass
    os.makedirs(results_path)
    for n, p in enumerate(glob.glob(path + '/*')):
        image = cv2.imread(p)
        if image is None:
            continue
        shutil.copy(p, '%s/%.5da.%s' % (results_path, n, p.rsplit('.', 1)[-1]))
        for k, m in enumerate(lp.analyze_cropped(image)):
            m = '/home/brandyn/projects/crawlers/goodlogo/entity_images/%s/%s' % (str(m['entity']), str(m['file']))
            if k == 0:
                print((k, p, m))
            out_path = '%s/%.5db-%.3d.%s' % (results_path, n, k, p.rsplit('.', 1)[-1])
            shutil.copy(m, out_path)


def writetb_parts(path, kvs, num_per_file, **kw):
    out = []
    part_num = 0
    def _flush(out, part_num):
        hadoopy.writetb('%s/part-%.5d' % (path, part_num), out, **kw)
        return [], part_num + 1
    for kv in kvs:
        print(kv[0])
        out.append(kv)
        if len(out) >= num_per_file:
            out, part_num = _flush(out, part_num)
    if out:
        out, part_num = _flush(out, part_num)


def get_logos():
    path = '/home/brandyn/projects/crawlers/goodlogo/entity_images/'
    for entity_path in glob.glob(path + '/*'):
        for fn in glob.glob(entity_path + '/*'):
            yield json.dumps([os.path.basename(entity_path), os.path.basename(fn)]), open(fn).read()


def put_logos_on_hadoop():
    writetb_parts('picarus/logos', get_logos(), 10)


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        if not hadoopy.exists('picarus/logos'):
            put_logos_on_hadoop()
        lp = LogoProcessor()
        hdfs_path = 'picarus/logos'
        #lp.compute_db_hadoop(hdfs_path)
        with open('index.pb') as fp:
            lp.load(fp.read())
        print lp.index._hashes.shape
        compare_to_local(lp)

if __name__ == '__main__':
    unittest.main()
