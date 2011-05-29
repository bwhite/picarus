"""Hadoopy Image Clustering Utility"""
import argparse


def _parse():
    parser = argparse.ArgumentParser(description='Hadoopy Image Clustering Utility')
    sps = parser.add_subparsers(help='Available commands (select for additional help)')

    # Image Feature
    sp = sps.add_parser('image_feature', help='Compute features on entire image')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('feature', type=str, help='Image feature to use (from features.py)')

    # Face Feature
    sp = sps.add_parser('face_feature', help='Extract faces and compute features on them')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('feature', type=str, help='Image feature to use (from features.py)')

    # Whiten Features
    sp = sps.add_parser('whiten', help='Scale features to zero mean unit variance')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')

    # Uniform Sample
    sp = sps.add_parser('sample', help='Uniformly sample a specified number of features (random clustering)')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('num_clusters', type=int, help='Desired number of clusters')

    # K-Means Cluster
    sp = sps.add_parser('kmeans', help='K-Means Cluster')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('num_clusters', type=int, help='Desired number of clusters')
    sp.add_argument('metric', type=str, help='Distance metric to use (from metrics.py)')
    sp.add_argument('num_iters', type=str, help='Maximum number of iterations')

    # Hierarchical Agglomerative Clustering
    sp = sps.add_parser('hac', help='Hierarhical Agglomerative Clustering')
    sp.add_argument('input', type=str, help='HDFS Input')
    sp.add_argument('output', type=str, help='HDFS Output')
    sp.add_argument('metric', type=str, help='Distance metric to use (from metrics.py)')

    # Visualize Clusters
    sp = sps.add_parser('visualize', help='Visualize clusters')
    sp.add_argument('input', type=str, help='HDFS Input')

    args = parser.parse_args()
    #return args.dir_in, args.seq_out
_parse()
