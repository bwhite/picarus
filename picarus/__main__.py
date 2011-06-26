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
    _picarus.vision.__main__._parser(sps.add_parser('vision', help='Computer vision functionality').add_subparsers(help='Vision commands'))
    _picarus.classify.__main__._parser(sps.add_parser('classify', help='Classification functionality').add_subparsers(help='Classification commands'))
    _picarus.cluster.__main__._parser(sps.add_parser('cluster', help='Clustering functionality').add_subparsers(help='Cluster commands'))

    # Report Categories from Prediction Output
    #s = sps.add_parser('report_categories', help='Report Categories from Prediction Output')
    #s.add_argument('hdfs_join_predictions_input', **ca['input'])
    #s.add_argument('local_output', help='report output')
    #s.add_argument('--image_limit', help='fill each category with <image_limit> highest confidences',
    #                type=int, default=200)
    #s.add_argument('--local_thumb_output', help='folder of image thumbnails', default=None)
    #s.set_defaults(func=_picarus.report.report_categories)

    # Report Clustering
    #s = sps.add_parser('report_clusters', help='Report Clusters')
    #s.add_argument('hdfs_input', **ca['input'])
    #s.add_argument('local_json_output', help='report output')
    #s.add_argument('category', help='category tag for this clustering')
    #s.add_argument('--sample', help='sample size', type=int, default=20)
    #s.add_argument('--make_faces', action="store_true")
    #s.set_defaults(func=_picarus.report.report_clusters)

    # Report Video Keyframes
    #s = sps.add_parser('report_video_keyframe', help='Report Video Keyframes')
    #s.add_argument('hdfs_input', **ca['input'])
    #s.add_argument('local_json_output', help='report output')
    #s.add_argument('--local_thumb_output', help='local thumbnail output directory')
    #s.set_defaults(func=_picarus.report.report_video_keyframe)

    # Local Thumbnail Output
    #s = sps.add_parser('report_thumbnails', help='Report Categories from Face Clustering')
    #s.add_argument('hdfs_input', **ca['input'])
    #s.add_argument('local_thumb_output', help='local thumbnail output directory')
    #s.set_defaults(func=_picarus.report.report_thumbnails)

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    _main()
