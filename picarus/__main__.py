"""Hadoopy Image Clustering Utility"""
import argparse as _argparse
import picarus as _picarus

_ca = {'input': {'help': 'HDFS Input'},
       'output': {'help': 'HDFS Output'},
       'image_data': {'help': 'HDFS image data key=unique_id value=binary_image_data'},
       'feature': {'help': 'Image feature to use from features.py (default: hist_joint)', 'default': 'hist_joint'},
       'classifier': {'help': 'Image feature to use from features.py (default: hist_joint)', 'default': 'hist_joint'},
       'num_clusters': {'type': int, 'help': 'Desired number of clusters'},
       'image_length': {'type': int, 'help': 'Side length of image before feature computation (default: 256)', 'default': 256},
       'metric': {'help': 'Distance metric to use from metrics.py (default l2sqr)', 'default': 'l2sqr'}}


def _main():
    parser = _argparse.ArgumentParser(description='Hadoopy Image Clustering Utility')
    sps = parser.add_subparsers(help='Available commands (select for additional help)')
    import picarus.vision.__main__
    import picarus.cluster.__main__
    import picarus.classify.__main__
    import picarus.report.__main__
    import picarus.io.__main__
    _picarus.vision.__main__._parser(sps.add_parser('vision', help='Computer vision functionality').add_subparsers(help='Vision commands'))
    _picarus.classify.__main__._parser(sps.add_parser('classify', help='Classification functionality').add_subparsers(help='Classification commands'))
    _picarus.cluster.__main__._parser(sps.add_parser('cluster', help='Clustering functionality').add_subparsers(help='Cluster commands'))
    _picarus.report.__main__._parser(sps.add_parser('report', help='Reporting functionality').add_subparsers(help='Report commands'))
    _picarus.io.__main__._parser(sps.add_parser('io', help='Input/Output functionality').add_subparsers(help='IO commands'))

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    _main()
