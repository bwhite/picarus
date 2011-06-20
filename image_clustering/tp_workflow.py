
import cluster
import time


def train():
    # HDFS Paths for Output
    start_time = time.time()
    root = '/user/brandyn/tp/image_cluster/run-%f/' % start_time
    
    # HDFS Paths with data of the form (unique_string, binary_image_data
    train_photos_path = ''
    train_nonphotos_path = ''
    train_indoor_path = '/user/brandyn/indoors'
    train_outdoor_path = '/user/brandyn/outdoors'
    train_objects_path = ''
    train_nonobjects_path = ''
    train_pr0n_path = ''
    train_nonpr0n_path = ''
    train_faces_path = ''
    train_nonfaces_path = ''

    # Compute features for classifier train
    cluster.run_image_feature(train_photos_path, root + 'train_feat/photos', 'hist_joint', 256)
    cluster.run_image_feature(train_nonphotos_path, root + 'train_feat/nonphotos', 'hist_joint', 256)
    cluster.run_image_feature(train_indoor_path, root + 'train_feat/indoor', 'hist_joint', 256)
    cluster.run_image_feature(train_outdoor_path, root + 'train_feat/outdoor', 'hist_joint', 256)
    cluster.run_image_feature(train_objects_path, root + 'train_feat/objects', 'hist_joint', 256)
    cluster.run_image_feature(train_nonobjects_path, root + 'train_feat/nonobjects', 'hist_joint', 256)
    cluster.run_image_feature(train_pr0n_path, root + 'train_feat/pr0n', 'hist_joint', 256)
    cluster.run_image_feature(train_nonpr0n_path, root + 'train_feat/nonpr0n', 'hist_joint', 256)
    cluster.run_image_feature(train_faces_path, root + 'train_feat/faces', 'hist_joint', 256)
    cluster.run_image_feature(train_nonfaces_path, root + 'train_feat/nonfaces', 'hist_joint', 256)

    # Label images # TODO make one run of this per feature type as the training assumes the features are homogeneous
    cluster.run_classifier_labels(root + 'train_feat/photos', root + 'train_feat/nonphotos', root + 'labels/photos',
                                  'photo', '', 'tp_photos_labels.js', 'svmlinear')
    cluster.run_classifier_labels(root + 'train_feat/indoor', root + 'train_feat/outdoor', root + 'labels/indoor',
                                  'indoor', '', 'tp_indoor_labels.js', 'svmlinear')
    cluster.run_classifier_labels(root + 'train_feat/objects', root + 'train_feat/nonobjects', root + 'labels/objects',
                                  'object', '', 'tp_objects_labels.js', 'svmlinear')
    cluster.run_classifier_labels(root + 'train_feat/pr0n', root + 'train_feat/nonpr0n', root + 'labels/pr0n',
                                  'pr0n', '', 'tp_pr0n_labels.js', 'svmlinear')
    cluster.run_classifier_labels(root + 'train_feat/faces', root + 'train_feat/nonfaces', root + 'labels/faces',
                                  'face', '', 'tp_faces_labels.js', 'svmlinear')

    # Train classifiers
    cluster.run_train_classifier([root + 'train_feat/photos', root + 'train_feat/nonphotos'], root + 'classifiers/photos', 'tp_photos_labels.js')
    cluster.run_train_classifier([root + 'train_feat/indoor', root + 'train_feat/outdoor'], root + 'classifiers/indoor', 'tp_indoor_labels.js')
    cluster.run_train_classifier([root + 'train_feat/objects', root + 'train_feat/nonobjects'], root + 'classifiers/objects', 'tp_objects_labels.js')
    cluster.run_train_classifier([root + 'train_feat/pr0n', root + 'train_feat/nonpr0n'], root + 'classifiers/pr0n', 'tp_pr0n_labels.js')
    cluster.run_train_classifier([root + 'train_feat/faces', root + 'train_feat/nonfaces'], root + 'classifiers/faces', 'tp_faces_labels.js')
    
if __name__ == '__main__':
    train()
