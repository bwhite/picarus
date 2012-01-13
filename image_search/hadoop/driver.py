import hadoopy
import time

now = time.time()
#flickr_dir = '/user/brandyn/flickr_data/run-1325960005.138596/out/flickr_join2'
flickr_dir = '/mnt/out/part-00000'
features_dir = 'features-%f' % now
median_dir = 'median-%f' % now
hashes_dir = 'hashes-%f' % now

hadoopy.launch_frozen(flickr_dir, features_dir, 'build_features.py')
hadoopy.launch_frozen(features_dir, median_dir, 'calc_median_feature.py')
#hadoopy.launch_frozen(features_dir, hashes_dir, 'compute_hashes.py') 

