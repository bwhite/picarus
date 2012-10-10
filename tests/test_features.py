try:
    import unittest2 as unittest
except ImportError:
    import unittest
import picarus._features
import picarus._importer
import cPickle as pickle
import cv2
import json
import numpy as np


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        "Test that serializing clusters to json results in the same feature output"
        clusters = pickle.load(open(picarus.__path__[0] + '/vision/data/hog_8_2_clusters.pkl'))
        image = cv2.imread('lena.jpg')
        f0 = picarus._features._bovw_hog(clusters)
        o0 = f0(image)
        js = json.dumps({'name': 'picarus._features._bovw_hog', 'kw': {'clusters': clusters.tolist()}})
        f1 = picarus._importer.call_import(json.loads(js))
        o1 = f1(image)
        np.testing.assert_equal(o0, o1)

if __name__ == '__main__':
    unittest.main()
