"""Hadoopy Image Clustering Utility"""
import argparse
import hadoopy


def _run_image_feature(input, output, **kw):
    hadoopy.launch_frozen(input, output, 'feature_compute.py', reducer=False)


def _run_face_feature(**kw):
    pass


def _run_whiten(**kw):
    pass


def _run_sample(input, output, num_clusters, **kw):
    hadoopy.launch_frozen(input, output, 'random_sample.py',
                          cmdenvs=['SAMPLE_SIZE=%d' % num_clusters])


def _run_kmeans(**kw):
    pass


def _run_hac(**kw):
    pass


def _run_visualize(**kw):
    pass


def main():
    parser = argparse.ArgumentParser(description='Hadoopy Image Clustering Utility')
    sps = parser.add_subparsers(help='Available commands (select for additional help)')

    # Image Feature
    sp = sps.add_parser('image_feature', help='Compute features on entire image')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('feature', type=str, help='Image feature to use (from features.py)')
    sp.set_defaults(func=_run_image_feature)

    # Face Feature
    sp = sps.add_parser('face_feature', help='Extract faces and compute features on them')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('feature', type=str, help='Image feature to use (from features.py)')
    sp.set_defaults(func=_run_face_feature)

    # Whiten Features
    sp = sps.add_parser('whiten', help='Scale features to zero mean unit variance')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.set_defaults(func=_run_whiten)

    # Uniform Sample
    sp = sps.add_parser('sample', help='Uniformly sample a specified number of features (random clustering)')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('num_clusters', type=int, help='Desired number of clusters')
    sp.set_defaults(func=_run_sample)

    # K-Means Cluster
    sp = sps.add_parser('kmeans', help='K-Means Cluster')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('num_clusters', type=int, help='Desired number of clusters')
    sp.add_argument('metric', type=str, help='Distance metric to use (from metrics.py)')
    sp.add_argument('num_iters', type=str, help='Maximum number of iterations')
    sp.set_defaults(func=_run_kmeans)

    # Hierarchical Agglomerative Clustering
    sp = sps.add_parser('hac', help='Hierarhical Agglomerative Clustering')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('metric', type=str, help='Distance metric to use (from metrics.py)')
    sp.set_defaults(func=_run_hac)

    # Visualize Clusters
    sp = sps.add_parser('visualize', help='Visualize clusters')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.set_defaults(func=_run_visualize)

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()
