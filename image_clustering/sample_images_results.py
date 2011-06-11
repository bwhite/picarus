import hadoopy
import os
import time
import json

out_path = 'out/cluster/%f/' % time.time()
image_path = '%s/images/' % (out_path)
os.makedirs(image_path)
groups = {}
#/user/brandyn/tp/image_cluster/run-15//samples
for group, (image_name, image_data) in hadoopy.readtb('/user/brandyn/tp/face_cluster/run-13//samples'):
    image_name = image_name + '.jpg'
    with open(image_path + image_name, 'w') as fp:
        fp.write(image_data) 
    print(image_path + image_name)
    groups.setdefault(int(group), {'all_images': [], 'sample_images': [], 'size': 0})['sample_images'].append(image_name)

with open(out_path + 'cluster.js', 'w') as fp:
    json.dump(groups.values(), fp)
