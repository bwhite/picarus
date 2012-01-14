import hadoopy
import time
import cPickle as pickle
import numpy as np

def compute_database(flickr_data):
    r = 'image_search/%f/' % time.time()
    f_path = r + 'features/'
    m_path = r + 'median/'
    h_path = r + 'hashes/'
    j_path = r + 'hash_metadata/'
    hadoopy.launch_frozen(flickr_data, f_path, 'build_features.py')
    hadoopy.launch_frozen(f_path, m_path, 'calc_median_feature.py')
    median = np.array([x for _, x in sorted(hadoopy.readtb(m_path))])
    pickle.dump(median, open('median.pkl', 'w'), -1)
    hadoopy.launch_frozen(f_path, h_path, 'compute_hashes.py', files=['median.pkl'])
    hadoopy.launch_frozen([h_path, flickr_data], j_path, 'join.py',
                          num_reducers=10)
    hashes, metadatas = zip(*[x[1] for x in hadoopy.readtb(j_path)])
    with open('database.pkl', 'w') as fp:
        pickle.dump((hashes, metadatas, median), fp, -1)

compute_database('/user/brandyn/flickr_data_picarus/run-1326494695.490887/out/flickr_images')
