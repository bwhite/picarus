"""Hadoopy Image Clustering Utility"""
import argparse
import hadoopy
import tempfile
import os
import cPickle as pickle
import numpy as np
import glob
import file_parse


def run_image_feature(hdfs_input, hdfs_output, feature, image_length, **kw):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'feature_compute.py', reducer=False,
                          cmdenvs=['IMAGE_LENGTH=%d' % image_length,
                                   'FEATURE=%s' % feature],
                          files=['eigenfaces_lfw_cropped.pkl'])


def run_face_finder(hdfs_input, hdfs_output, image_length, **kw):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'face_finder.py', reducer=False,
                          cmdenvs=['IMAGE_LENGTH=%d' % image_length],
                          files=['haarcascade_frontalface_default.xml'])


def run_whiten(**kw):
    pass


def run_sample(hdfs_input, hdfs_output, num_clusters, **kw):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'random_sample.py',
                          cmdenvs=['SAMPLE_SIZE=%d' % num_clusters])


def run_kmeans(hdfs_input, hdfs_prev_clusters, hdfs_image_data, hdfs_output, num_clusters,
               num_iters, num_samples, metric, local_json_output=None, **kw):
    frozen_tar_path = None
    for cur_iter_num in range(num_iters):
        clusters_fp = fetch_clusters_from_hdfs(hdfs_prev_clusters)
        clusters_fn = os.path.basename(clusters_fp.name)
        cur_output = '%s/clust%.6d' % (hdfs_output, cur_iter_num)
        _, frozen_tar_path = hadoopy.launch_frozen(hdfs_input, cur_output, 'kmeans.py',
                                                   cmdenvs=['CLUSTERS_FN=%s' % clusters_fn],
                                                   files=[clusters_fp.name],
                                                   num_reducers=max(1, num_clusters / 2),
                                                   frozen_tar_path=frozen_tar_path)
        hdfs_prev_clusters = cur_output
    print('Clusters[%s]' % hdfs_prev_clusters)
    # Compute K-Means assignment/samples
    # TODO Do full assignment, then sample
    clusters_fp = fetch_clusters_from_hdfs(hdfs_prev_clusters)
    clusters_fn = os.path.basename(clusters_fp.name)
    cur_output = '%s/assign' % hdfs_output
    hadoopy.launch_frozen(hdfs_input, cur_output, 'kmeans_assign.py',
                          cmdenvs=['CLUSTERS_FN=%s' % clusters_fn,
                                   'NUM_SAMPLES=%d' % num_samples,
                                   'mapred.text.key.partitioner.options=-k1'],
                          files=[clusters_fp.name],
                          num_reducers=max(1, num_clusters / 2),
                          partitioner='org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner')
    print('Assignment[%s]' % cur_output)
    # Filter the samples
    assignments_fp = fetch_assignments_from_hdfs(cur_output)
    assignments_fn = os.path.basename(assignments_fp.name)
    cur_output = '%s/samples' % hdfs_output
    hadoopy.launch_frozen(hdfs_image_data, cur_output, 'filter_samples.py',
                          cmdenvs=['ASSIGNMENTS_FN=%s' % os.path.basename(assignments_fn)],
                          files=[assignments_fp.name],
                          reducer=None)
    print('Samples[%s]' % cur_output)


def run_hac(**kw):
    pass


def run_visualize(**kw):
    pass


def fetch_clusters_from_hdfs(hdfs_input):
    """Fetch remote clusters and store locally

    Clusters are sorted to allow comparing between iterations

    Args:
        hdfs_input: HDFS input path

    Returns:
        NamedTemporaryFile holding the cluster data
    """
    clusters_fp = tempfile.NamedTemporaryFile()
    clusters = [v.tolist() for k, v in hadoopy.readtb(hdfs_input)]
    clusters.sort()
    clusters = np.ascontiguousarray(clusters, dtype=np.float64)
    pickle.dump(clusters, clusters_fp, -1)
    clusters_fp.seek(0)
    return clusters_fp


def fetch_assignments_from_hdfs(hdfs_input):
    """Fetch remote assignments and store locally

    Args:
        hdfs_input: HDFS input path

    Returns:
        NamedTemporaryFile holding the assignment data
    """
    assignments_fp = tempfile.NamedTemporaryFile()
    assignments = list(hadoopy.readtb(hdfs_input))
    pickle.dump(assignments, assignments_fp, -1)
    assignments_fp.seek(0)
    return assignments_fp


def run_classifier_labels(hdfs_input_pos, hdfs_input_neg, hdfs_output, classifier_name, classifier_extra, local_labels, classifier, **kw):
    labels = {}
    try:
        labels = file_parse.load(local_labels)
    except IOError:
        pass
    hdfs_output_pos = hdfs_output + '/pos'
    hdfs_output_neg = hdfs_output + '/neg'
    hadoopy.launch_frozen(hdfs_input_pos, hdfs_output_pos, 'collect_keys.py')
    hadoopy.launch_frozen(hdfs_input_neg, hdfs_output_neg, 'collect_keys.py')
    pos_keys = sum((x[1] for x in hadoopy.readtb(hdfs_output_pos)), [])
    neg_keys = sum((x[1] for x in hadoopy.readtb(hdfs_output_neg)), [])
    labels[classifier_name] = {'labels': {'1': pos_keys, '-1': neg_keys},
                               'classifier': classifier,
                               'classifier_extra': classifier_extra}
    file_parse.dump(labels, local_labels)


def run_train_classifier(hdfs_input, hdfs_output, local_labels, **kw):
    import classipy
    # NOTE: Adds necessary files
    files = glob.glob(classipy.__path__[0] + "/lib/*")
    files.append(local_labels)
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'train_classifier.py',
                          files=files,
                          cmdenvs=['LOCAL_LABELS_FN=%s' % os.path.basename(local_labels)])


def run_predict_classifier(hdfs_input, hdfs_classifier_input, hdfs_output, **kw):
    import classipy
    # NOTE: Adds necessary files
    files = glob.glob(classipy.__path__[0] + "/lib/*")
    with tempfile.NamedTemporaryFile(suffix='.pkl.gz') as fp:
        file_parse.dump(list(hadoopy.readtb(hdfs_classifier_input)), fp.name)
        files.append(fp.name)
        hadoopy.launch_frozen(hdfs_input, hdfs_output, 'predict_classifier.py',
                              files=files, reducer=None,
                              cmdenvs=['CLASSIFIERS_FN=%s' % os.path.basename(fp.name)])


def main():
    parser = argparse.ArgumentParser(description='Hadoopy Image Clustering Utility')
    sps = parser.add_subparsers(help='Available commands (select for additional help)')

    ca = {'input': {'help': 'HDFS Input'},
          'output': {'help': 'HDFS Output'},
          'image_data': {'help': 'HDFS image data key=unique_id value=binary_image_data'},
          'feature': {'help': 'Image feature to use from features.py (default: hist_joint)', 'default': 'hist_joint'},
          'classifier': {'help': 'Image feature to use from features.py (default: hist_joint)', 'default': 'hist_joint'},
          'num_clusters': {'type': int, 'help': 'Desired number of clusters'},
          'image_length': {'type': int, 'help': 'Side length of image before feature computation (default: 256)', 'default': 256},
          'metric': {'help': 'Distance metric to use from metrics.py (default l2sqr)', 'default': 'l2sqr'}}

    # Image Feature
    sp = sps.add_parser('image_feature', help='Compute features on entire image')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('--feature', **ca['feature'])
    sp.add_argument('--image_length', **ca['image_length'])
    sp.set_defaults(func=run_image_feature)

    # Make labels pkl
    sp = sps.add_parser('classifier_labels', help='Given positive/negative inputs, make/update the labels .pkl for training the classifier')
    sp.add_argument('hdfs_input_pos', **ca['input'])
    sp.add_argument('hdfs_input_neg', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('classifier_name', help='Name to give the classifier (e.g., indoor_outdoor).  This is used by the classifier training.')
    sp.add_argument('local_labels', help='Path to labels file, this can be an existing file and any existing classifier_name entry is replaced.')
    sp.add_argument('--classifier', help='Classifier to use from classifiers.py (default: svmlinear)', default='svmlinear')
    sp.add_argument('--classifier_extra', help='Additional data to pass to classifier (e.g., parameters). (default: '')', default='')
    sp.set_defaults(func=run_classifier_labels)

    # Train Classifier (take in features from the previous labeling step)
    sp = sps.add_parser('train_classifier', help='Train classifier on feature vectors')
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('local_labels', help='Path to labels file, this can be an existing file and any existing classifier_name entry is replaced.')
    sp.add_argument('hdfs_input', nargs='+', **ca['input'])
    sp.set_defaults(func=run_train_classifier)

    # Predict Classifier
    sp = sps.add_parser('predict_classifier', help='Predict classifier on feature vectors')
    sp.add_argument('hdfs_classifier_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('hdfs_input', nargs='+', **ca['input'])
    sp.set_defaults(func=run_predict_classifier)

    # Face Finder
    sp = sps.add_parser('face_finder', help='Extract faces')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('--image_length', **ca['image_length'])
    sp.set_defaults(func=run_face_finder)

    # Whiten Features
    sp = sps.add_parser('whiten', help='Scale features to zero mean unit variance')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.set_defaults(func=run_whiten)

    # Uniform Sample
    sp = sps.add_parser('sample', help='Uniformly sample a specified number of features (random clustering)')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('num_clusters', **ca['num_clusters'])
    sp.add_argument('--local_json_output', help='Local output path')  # TODO: Implement
    sp.set_defaults(func=run_sample)

    # K-Means Cluster
    sp = sps.add_parser('kmeans', help='K-Means Cluster')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_prev_clusters', help='HDFS path to previous clusters')
    sp.add_argument('hdfs_image_data', **ca['image_data'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('num_clusters', **ca['num_clusters'])
    sp.add_argument('num_iters', type=int, help='Maximum number of iterations')
    sp.add_argument('num_samples', type=int, help='Number of samples')
    sp.add_argument('--metric', **ca['metric'])
    sp.add_argument('--local_json_output', help='Local output path')
    sp.set_defaults(func=run_kmeans)

    # Hierarchical Agglomerative Clustering
    sp = sps.add_parser('hac', help='Hierarhical Agglomerative Clustering')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('--metric', **ca['metric'])
    sp.set_defaults(func=run_hac)

    # Visualize Clusters
    sp = sps.add_parser('visualize', help='Visualize clusters')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.set_defaults(func=run_visualize)

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()
