import pycassa
import json
import cPickle as pickle

config = dict(
    credentials={'username': 'amiller', 'password': 'F6E1A36701517F495F938'},
    keyspace='andrew_keyspace',
    cf_images='amiller_images',
    cf_features='amiller_features',
    )

pool = None
manager = None
cf_images = None
cf_features = None


def connect():
    global pool, manager, cf_images, cf_features
    pool = pycassa.ConnectionPool(config['keyspace'],
                                  ['vitrieve03.pc.umiacs.umd.edu:9160',
                                   'vitrieve02.pc.umiacs.umd.edu:9160',
                                   'vitrieve01.pc.umiacs.umd.edu:9160'],
                                  credentials=config['credentials'],
                                  pool_size=9)

    # System manager connects to the first in the pool
    manager = pycassa.system_manager.SystemManager(pool.server_list[0],
                                                   config['credentials'])

    cf_images = pycassa.ColumnFamily(pool, config['cf_images'])
    cf_features = pycassa.ColumnFamily(pool, config['cf_features'])


def get_image_hashes():
    # TODO: range scan for the meta data?
    return [_[0] for _ in
            cf_images.get('image_metadata', column_count=2000000000).items()]


def get_imagedata(im_hash):
    return cf_images.get('image_data', columns=[im_hash],
                         column_count=1)[im_hash]


def put_image(im_hash, data, metadata={}):
    cf_images.insert('image_data', {im_hash: data})
    cf_images.insert('image_metadata', {im_hash: json.dumps(metadata)})


def put_feature_value(feature_str, im_hash, value):
    """Insert a feature value using the feature identifier
    as a row key, and the image hash as the column key

    TODO Make the feature identifier include more than just the feature's name,
    such as the timestamp or a version string or a hash of the file
    """
    _ = cf_features.insert(feature_str,
                           {im_hash: pickle.dumps(value, -1)})
    return _


def feature_row_id(feature):
    return 'feature_%s' % str(type(feature))


def get_available_features():
    return [_[0] for _ in cf_features.get_range(column_count=1)]


def get_feature_values(feature, hashes=[]):
    return [pickle.loads(_[1])
            for _ in cf_features.get(feature_row_id(feature),
                                           hashes).items()]
