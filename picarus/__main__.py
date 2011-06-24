"""Hadoopy Image Clustering Utility"""
import argparse as _argparse
import picarus as _picarus


def _main():
    parser = _argparse.ArgumentParser(description='Hadoopy Image Clustering Utility')
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
    sp.set_defaults(func=_picarus.vision.run_image_feature)

    # Make labels pkl
    sp = sps.add_parser('classifier_labels', help='Given positive/negative inputs, make/update the labels .pkl for training the classifier')
    sp.add_argument('hdfs_input_pos', **ca['input'])
    sp.add_argument('hdfs_input_neg', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('classifier_name', help='Name to give the classifier (e.g., indoor_outdoor).  This is used by the classifier training.')
    sp.add_argument('local_labels', help='Path to labels file, this can be an existing file and any existing classifier_name entry is replaced.')
    sp.add_argument('--classifier', help='Classifier to use from classifiers.py (default: svmlinear)', default='svmlinear')
    sp.add_argument('--classifier_extra', help='Additional data to pass to classifier (e.g., parameters). (default: '')', default='')
    sp.set_defaults(func=_picarus.classify.run_classifier_labels)

    # Train Classifier (take in features from the previous labeling step)
    sp = sps.add_parser('train_classifier', help='Train classifier on feature vectors')
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('local_labels', help='Path to labels file, this can be an existing file and any existing classifier_name entry is replaced.')
    sp.add_argument('hdfs_input', nargs='+', **ca['input'])
    sp.set_defaults(func=_picarus.classify.run_train_classifier)

    # Predict Classifier
    sp = sps.add_parser('predict_classifier', help='Predict classifier on feature vectors')
    sp.add_argument('hdfs_classifier_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('hdfs_input', nargs='+', **ca['input'])
    sp.set_defaults(func=_picarus.classify.run_predict_classifier)

    # Join Predictions with Classifier
    sp = sps.add_parser('join_predictions', help='Joint predictions with images')
    sp.add_argument('hdfs_predictions_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('hdfs_input', nargs='+', **ca['input'])
    sp.add_argument('--local_image_output', help='Path to store local images', default='')
    sp.set_defaults(func=_picarus.classify.run_join_predictions)

    # Face Finder
    sp = sps.add_parser('face_finder', help='Extract faces')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('--image_length', **ca['image_length'])
    sp.add_argument('--boxes', help='If True make the value (image_data, boxes) where boxes is a list of (x, y, h, w)', type=bool, default=False)
    sp.set_defaults(func=_picarus.vision.run_face_finder)

    # Whiten Features
    sp = sps.add_parser('whiten', help='Scale features to zero mean unit variance')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.set_defaults(func=_picarus.cluster.run_whiten)

    # Uniform Sample
    sp = sps.add_parser('sample', help='Uniformly sample a specified number of features (random clustering)')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('num_clusters', **ca['num_clusters'])
    sp.add_argument('--local_json_output', help='Local output path')  # TODO: Implement
    sp.set_defaults(func=_picarus.cluster.run_sample)

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
    sp.set_defaults(func=_picarus.cluster.run_kmeans)

    # Hierarchical Agglomerative Clustering
    sp = sps.add_parser('hac', help='Hierarhical Agglomerative Clustering')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('--metric', **ca['metric'])
    sp.set_defaults(func=_picarus.cluster.run_hac)

    # Run Video Keyframing
    sp = sps.add_parser('video_keyframe', help='Run Video Keyframing')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('min_resolution', type=int, help='Maximum number of keyframes in each cluster')
    sp.add_argument('max_resolution', type=float, help='Minimum number seconds between keyframes')
    sp.add_argument('--ffmpeg', help='Use frozen ffmpeg binary instead of pyffmpeg (works with more kinds of encoded videos, poorly enocded videos)', action='store_true')
    sp.set_defaults(func=_picarus.vision.run_video_keyframe)

    # Report Categories from Prediction Output
    sp = sps.add_parser('report_categories', help='Report Categories from Prediction Output')
    sp.add_argument('hdfs_join_predictions_input', **ca['input'])
    sp.add_argument('local_output', help='report output')
    sp.add_argument('--image_limit', help='fill each category with <image_limit> highest confidences',
                    type=int, default=200)
    sp.add_argument('--local_thumb_output', help='folder of image thumbnails', default=None)
    sp.set_defaults(func=_picarus.report.report_categories)

    # Report Clustering
    sp = sps.add_parser('report_clusters', help='Report Clusters')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('local_json_output', help='report output')
    sp.add_argument('category', help='category tag for this clustering')
    sp.add_argument('--sample', help='sample size', type=int, default=20)
    sp.add_argument('--make_faces', action="store_true")
    sp.set_defaults(func=_picarus.report.report_clusters)

    # Report Video Keyframes
    sp = sps.add_parser('report_video_keyframe', help='Report Video Keyframes')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('local_json_output', help='report output')
    sp.add_argument('--local_thumb_output', help='local thumbnail output directory')
    sp.set_defaults(func=_picarus.report.report_video_keyframe)

    # Local Thumbnail Output
    sp = sps.add_parser('report_thumbnails', help='Report Categories from Face Clustering')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('local_thumb_output', help='local thumbnail output directory')
    sp.set_defaults(func=_picarus.report.report_thumbnails)

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    _main()
