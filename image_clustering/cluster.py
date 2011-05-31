"""Hadoopy Image Clustering Utility"""
import argparse
import hadoopy
import tempfile
import os
import cPickle as pickle
import numpy as np


def run_image_feature(input, output, feature='hist_joint', **kw):
    hadoopy.launch_frozen(input, output, 'feature_compute.py', reducer=False)


def run_face_feature(**kw):
    pass


def run_whiten(**kw):
    pass


def run_sample(input, output, num_clusters, **kw):
    hadoopy.launch_frozen(input, output, 'random_sample.py',
                          cmdenvs=['SAMPLE_SIZE=%d' % num_clusters])


def run_kmeans(input, prev_clusters, image_data, output, num_clusters,
               num_iters, num_samples, metric='l2sqr', json_output=None, **kw):
    for cur_iter_num in range(num_iters):
        clusters_fp = fetch_clusters_from_hdfs(prev_clusters)
        clusters_fn = os.path.basename(clusters_fp.name)
        cur_output = '%s/clust%.6d' % (output, cur_iter_num)
        hadoopy.launch_frozen(input, cur_output, 'kmeans.py',
                              cmdenvs=['CLUSTERS_FN=%s' % clusters_fn],
                              files=[clusters_fp.name],
                              num_reducers=max(1, num_clusters / 2))
        prev_clusters = cur_output
    print('Clusters[%s]' % prev_clusters)
    # Compute K-Means assignment/samples
    # TODO Do full assignment, then sample
    clusters_fp = fetch_clusters_from_hdfs(prev_clusters)
    clusters_fn = os.path.basename(clusters_fp.name)
    cur_output = '%s/assign' % output
    hadoopy.launch_frozen(input, cur_output, 'kmeans_assign.py',
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
    cur_output = '%s/samples' % output
    hadoopy.launch_frozen(image_data, cur_output, 'filter_samples.py',
                          cmdenvs=['ASSIGNMENTS_FN=%s' % assignments_fn],
                          files=[assignments_fp.name],
                          reducer=None)
    print('Samples[%s]' % cur_output)


def run_hac(**kw):
    pass


def run_visualize(**kw):
    pass


def fetch_clusters_from_hdfs(input):
    """Fetch remote clusters and store locally

    Clusters are sorted to allow comparing between iterations

    Args:
        input: HDFS input path

    Returns:
        NamedTemporaryFile holding the cluster data
    """
    clusters_fp = tempfile.NamedTemporaryFile()
    clusters = [v.tolist() for k, v in hadoopy.cat(input)]
    clusters.sort()
    clusters = np.ascontiguousarray(clusters, dtype=np.float64)
    pickle.dump(clusters, clusters_fp, -1)
    clusters_fp.seek(0)
    return clusters_fp


def fetch_assignments_from_hdfs(input):
    """Fetch remote assignments and store locally

    Args:
        input: HDFS input path

    Returns:
        NamedTemporaryFile holding the assignment data
    """
    assignments_fp = tempfile.NamedTemporaryFile()
    assignments = list(hadoopy.cat(input))
    pickle.dump(assignments, assignments_fp, -1)
    assignments_fp.seek(0)
    return assignments_fp


def main():
    parser = argparse.ArgumentParser(description='Hadoopy Image Clustering Utility')
    sps = parser.add_subparsers(help='Available commands (select for additional help)')

    ca = {'input': {'help': 'HDFS Input'},
          'output': {'help': 'HDFS Output'},
          'image_data': {'help': 'HDFS image data key=unique_id value=binary_image_data'},
          'feature': {'help': 'Image feature to use from features.py (default hsv_hist_joint)'},
          'num_clusters': {'type': int, 'help': 'Desired number of clusters'},
          'metric': {'help': 'Distance metric to use from metrics.py (default l2sqr)'}}

    # Image Feature
    sp = sps.add_parser('image_feature', help='Compute features on entire image')
    sp.add_argument('input', **ca['input'])
    sp.add_argument('output', **ca['output'])
    sp.add_argument('--feature', **ca['feature'])
    sp.set_defaults(func=run_image_feature)

    # Face Feature
    sp = sps.add_parser('face_feature', help='Extract faces and compute features on them')
    sp.add_argument('input', **ca['input'])
    sp.add_argument('output', **ca['output'])
    sp.add_argument('--feature', **ca['feature'])
    sp.set_defaults(func=run_face_feature)

    # Whiten Features
    sp = sps.add_parser('whiten', help='Scale features to zero mean unit variance')
    sp.add_argument('input', **ca['input'])
    sp.add_argument('output', **ca['output'])
    sp.set_defaults(func=run_whiten)

    # Uniform Sample
    sp = sps.add_parser('sample', help='Uniformly sample a specified number of features (random clustering)')
    sp.add_argument('input', **ca['input'])
    sp.add_argument('output', **ca['output'])
    sp.add_argument('num_clusters', **ca['num_clusters'])
    sp.add_argument('--json_output', help='Local output path')
    sp.set_defaults(func=run_sample)

    # K-Means Cluster
    sp = sps.add_parser('kmeans', help='K-Means Cluster')
    sp.add_argument('input', **ca['input'])
    sp.add_argument('prev_clusters', help='HDFS path to previous clusters')
    sp.add_argument('image_data', **ca['image_data'])
    sp.add_argument('output', **ca['output'])
    sp.add_argument('num_clusters', **ca['num_clusters'])
    sp.add_argument('num_iters', type=int, help='Maximum number of iterations')
    sp.add_argument('num_samples', type=int, help='Number of samples')
    sp.add_argument('--metric', **ca['metric'])
    sp.add_argument('--json_output', help='Local output path')
    sp.set_defaults(func=run_kmeans)

    # Hierarchical Agglomerative Clustering
    sp = sps.add_parser('hac', help='Hierarhical Agglomerative Clustering')
    sp.add_argument('input', **ca['input'])
    sp.add_argument('output', **ca['output'])
    sp.add_argument('--metric', **ca['metric'])
    sp.set_defaults(func=run_hac)

    # Visualize Clusters
    sp = sps.add_parser('visualize', help='Visualize clusters')
    sp.add_argument('input', **ca['input'])
    sp.set_defaults(func=run_visualize)

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()
