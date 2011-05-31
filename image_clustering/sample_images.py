import hadoopy
import os
import time

out_path = '/mnt/nfsdrives/shared/tp/cluster/%f/' % time.time()

for group, (image_name, image_data) in hadoopy.cat('/user/brandyn/tp/image_cluster/run-15//samples'):
    group_path = '%s/%d/' % (out_path, int(group))
    try:
        os.makedirs(group_path)
    except OSError:
        pass
    print(group_path + '%s.jpg' % image_name)
    with open(group_path + '%s.jpg' % image_name, 'w') as fp:
        fp.write(image_data)
