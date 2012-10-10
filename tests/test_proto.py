try:
    import unittest2 as unittest
except ImportError:
    import unittest
import picarus.api


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        si = picarus.api.SearchIndex()
        si.name = 'logos'
        raw_size = len(si.name)
        si.feature = '{"name": "Feature"}'
        raw_size += len(si.feature)
        si.hash = '{"name": "Hash"}'
        raw_size += len(si.hash)
        si.metric = '{"name": "Metric"}'
        raw_size += len(si.metric)
        si.feature_dims = 10
        raw_size += 4
        si.id_bytes = 4
        raw_size += 4
        si.hash_bytes = 8
        raw_size += 4
        si.index = 'sdfsdfsdf'
        raw_size += len(si.index)
        print('PB:[%d] Raw:[%d]' % (len(si.SerializeToString()), raw_size))

if __name__ == '__main__':
    unittest.main()