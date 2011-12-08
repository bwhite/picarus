import requests
import base64
import json
try:
    import unittest2 as unittest
except ImportError:
    import unittest
headers = {'content-type': 'application/json'}
auth = ('user', 'pass')
url = 'http://localhost:8080/'
image_urls = ['http://farm4.static.flickr.com/3267/3112736300_03ee1bb778.jpg',
              'http://farm6.static.flickr.com/5016/5540039736_8429b2e8ee.jpg',
              'http://farm2.static.flickr.com/1302/532195789_0a18ea91f4.jpg']

# Cheat Sheet (method/test) <http://docs.python.org/library/unittest.html>
#
# assertEqual(a, b)       a == b   
# assertNotEqual(a, b)    a != b    
# assertTrue(x)     bool(x) is True  
# assertFalse(x)    bool(x) is False  
# assertRaises(exc, fun, *args, **kwds) fun(*args, **kwds) raises exc
# assertAlmostEqual(a, b)  round(a-b, 7) == 0         
# assertNotAlmostEqual(a, b)          round(a-b, 7) != 0
# 
# Python 2.7+ (or using unittest2)
#
# assertIs(a, b)  a is b
# assertIsNot(a, b) a is not b
# assertIsNone(x)   x is None
# assertIsNotNone(x)  x is not None
# assertIn(a, b)      a in b
# assertNotIn(a, b)   a not in b
# assertIsInstance(a, b)    isinstance(a, b)
# assertNotIsInstance(a, b) not isinstance(a, b)
# assertRaisesRegexp(exc, re, fun, *args, **kwds) fun(*args, **kwds) raises exc and the message matches re
# assertGreater(a, b)       a > b
# assertGreaterEqual(a, b)  a >= b
# assertLess(a, b)      a < b
# assertLessEqual(a, b) a <= b
# assertRegexpMatches(s, re) regex.search(s)
# assertNotRegexpMatches(s, re)  not regex.search(s)
# assertItemsEqual(a, b)    sorted(a) == sorted(b) and works with unhashable objs
# assertDictContainsSubset(a, b)      all the key/value pairs in a exist in b
CLIENT_VERSION = {'major': 0, 'minor': 0, 'patch': 0, 'branch': 'dv'}
CLIENT_VERSION_PART = '"version":' + json.dumps(CLIENT_VERSION)


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_help_status(self):
        r = requests.get(url + 'help/configuration.json', headers=headers)
        content = json.loads(r.content)
        self.assertEqual(content['version'], CLIENT_VERSION)
        self.assertIn('max_request_size', content)
        self.assertIn('version', content)
        self.assertIn('time', content)
        self.assertEqual(r.status_code, 200)

    def test_help_test(self):
        r = requests.get(url + 'help/test.json', headers=headers)
        self.assertEqual(r.content, '"ok"')
        self.assertEqual(r.status_code, 200)

    def test_image_bad_auth(self):
        data = '{"data": [], "query": {}, %s}' % (CLIENT_VERSION_PART,)
        r = requests.put(url + 'analyze/tags.json', auth=('nobody', 'nobody'), data=data, headers=headers)
        print(r.content)
        self.assertEqual(r.status_code, 401)

    def test_image_b64(self):
        image_data_b64 = base64.b64encode(requests.get(image_urls[0]).content)
        data = '{"data": {"type": "image", "binary_b64": "%s"}, "query": {}, %s}' % (image_data_b64, CLIENT_VERSION_PART)
        r = requests.put(url + 'analyze/tags.json', auth=auth, data=data, headers=headers)
        print(r.content)
        self.assertEqual(r.status_code, 200)

    def test_image_url(self):
        data = '{"data": {"type": "image", "image_url": "%s"}, "query": {}, %s}' % (image_urls[0], CLIENT_VERSION_PART)
        r = requests.put(url + 'analyze/tags.json', auth=auth, data=data, headers=headers)
        print(r.content)
        self.assertEqual(r.status_code, 200)

    def test_image_url_multi(self):
        data = '{"data": [{"type": "image", "image_url": "%s"}, {"type": "image", "image_url": "%s"}], "query": {}, %s}' % (image_urls[0],
                                                                                                                            image_urls[1],
                                                                                                                            CLIENT_VERSION_PART)
        r = requests.put(url + 'analyze/tags.json', auth=auth, data=data, headers=headers)
        print(r.content)
        self.assertEqual(r.status_code, 200)

    def test_image_b64_url(self):
        image_data_b64 = base64.b64encode(requests.get(image_urls[0]).content)
        data = '{"data": {"type": "image", "binary_b64": "%s", "image_url": "%s"}, "query": {}, %s}' % (image_data_b64, image_urls[0], CLIENT_VERSION_PART)
        r = requests.put(url + 'analyze/tags.json', auth=auth, data=data, headers=headers)
        print(r.content)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
