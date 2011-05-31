import pycassa
import json
import cPickle as pickle
import itertools

config = dict(
    credentials={'username': 'amiller', 'password': 'F6E1A36701517F495F938'},
    keyspace='andrew_keyspace',
    cf_images='amiller_images',
    cf_features='amiller_features',
    )


def connect():
    """Connect to cassandra server using default credentials
    TODO Add an option to use credentials from a config file
    """
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


if not 'pool' in globals():
    pool = None
    manager = None
    cf_images = None
    cf_features = None
    connect()


def sorted_iter_diff(a, b):
    """Returns an iterator of the elements in a that are not in b.

    Arguments:
       a, b: Sorted iterators (e.g., items returned from get_range()
    """
    _a, _b = None, None
    try:
        while True:
            if _a == _b:
                _a = a.next()
                _b = b.next()
            elif _a < _b:
                yield _a
                _a = a.next()
            elif _a > _b: _b = b.next()
    except StopIteration:
        for _a in a: yield _a


def buffered_get_row(cf, row_key, buffer_size=500):
    """Returns a generator of ((column_name, column),...) values
    from a specific row, using a buffered read.

    Arguments:
        cf: column family, e.g. cass.cf_features
        row_key:
        buffer_size:
    """

    def gen():
        startColumn = ""
        try:
            while True:
                r = [_ for _ in cf.get(row_key,
                                       column_start=startColumn,
                                       column_count=buffer_size).items()]
                # Advance to the very next possible column \
                # (lexical sort on string)
                startColumn = r[-1][0] + '\x00'
                yield r
        except pycassa.NotFoundException:
            return

    return itertools.chain.from_iterable(gen())


def get_image_hashes():
    # TODO: range scan for the meta data?
    return (_[0] for _ in buffered_get_row(cf_images, 'image_metadata'))


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


def get_feature_hashes(feature_str, hashes=[]):
    return (_[0] for _ in buffered_get_row(cf_features, feature_str))
