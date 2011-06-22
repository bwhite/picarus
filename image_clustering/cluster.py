"""Hadoopy Image Clustering Utility"""
import argparse
import hadoopy
import tempfile
import os
import cPickle as pickle
import numpy as np
import glob
import file_parse
import report_output
import heapq
import StringIO
import Image
import re
import random
import vidfeat


def run_image_feature(hdfs_input, hdfs_output, feature, image_length, **kw):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'feature_compute.py', reducer=False,
                          cmdenvs=['IMAGE_LENGTH=%d' % image_length,
                                   'FEATURE=%s' % feature],
                          files=['eigenfaces_lfw_cropped.pkl'])


def run_face_finder(hdfs_input, hdfs_output, image_length, boxes, **kw):
    cmdenvs = ['IMAGE_LENGTH=%d' % image_length]
    if boxes:
        cmdenvs.append('OUTPUT_BOXES=True')
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'face_finder.py', reducer=False,
                          cmdenvs=cmdenvs,
                          files=['haarcascade_frontalface_default.xml'])


def run_whiten(hdfs_input, hdfs_output, **kw):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'whiten.py')


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
        frozen_tar_path = hadoopy.launch_frozen(hdfs_input, cur_output, 'kmeans.py',
                                                cmdenvs=['CLUSTERS_FN=%s' % clusters_fn],
                                                files=[clusters_fp.name],
                                                num_reducers=max(1, num_clusters / 2),
                                                frozen_tar_path=frozen_tar_path)['frozen_tar_path']
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


def report_categories(hdfs_join_predictions_input, local_output, image_limit, local_thumb_output, **kw):
    # Output a cluster for each category
    # FIXME This is hardcoded for indoor_outdoor, it will have to change when
    # there are multiple classifiers (indoor, outdoor, photos, documents, etc)
    hashes = {-1: [], 1: []}
    totals = {-1: 0, 1: 0}

    # First pass: find images for each category
    for image_hash, (classifier_preds, image_data) in hadoopy.readtb(hdfs_join_predictions_input):
        for classifier, preds in classifier_preds.items():
            posname, negname = classifier.split('_')
            for conf, label in preds:
                totals[label] += 1
                if len(hashes[label]) < image_limit:
                    heapq.heappush(hashes[label], (conf, image_hash))
                else:
                    heapq.heappushpop(hashes[label], (conf, image_hash))

    print negname, len(hashes[-1]), totals[-1]
    print posname, len(hashes[1]), totals[1]

    categories = {}
    categories[posname] = report_output.make_random_clusters([h for _, h in hashes[1]], posname)
    categories[negname] = report_output.make_random_clusters([h for _, h in hashes[-1]], negname)

    try:
        os.makedirs(os.path.dirname(local_output))
    except OSError:
        pass
    file_parse.dump(categories, local_output)

    # Second pass: make image thumbnails
    if local_thumb_output:
        try:
            os.makedirs(local_thumb_output)
        except OSError:
            pass
        hashset = set([h for _, h in hashes[-1] + hashes[1]])
        for image_hash, (classifier_preds, image_data) in hadoopy.readtb(hdfs_join_predictions_input):
            if image_hash in hashset:
                s = StringIO.StringIO()
                s.write(image_data)
                s.seek(0)
                frame = Image.open(s)
                frame.thumbnail((100,100))
                path = '%s/%s.jpg' % (local_thumb_output, image_hash)
                frame.save(path)


def run_join_predictions(hdfs_predictions_input, hdfs_input, hdfs_output, local_image_output, **kw):
    inputs = [hdfs_predictions_input]
    if isinstance(hdfs_input, list):
        inputs += hdfs_input
    else:
        inputs.append(hdfs_input)
    hadoopy.launch_frozen(inputs, hdfs_output, 'join_predictions.py')
    if local_image_output:
        for image_hash, (classifier_preds, image_data) in hadoopy.readtb(hdfs_output):
            for classifier, preds in classifier_preds.items():
                for conf, label in preds:
                    path = '%s/%s/label_%d/%8.8f-%s.jpg' % (local_image_output, classifier, label, conf, image_hash)
                    try:
                        os.makedirs(os.path.dirname(path))
                    except OSError:
                        pass
                    with open(path, 'w') as fp:
                        fp.write(image_data)


def run_thresh_predictions(hdfs_predictions_input, hdfs_input, hdfs_output, class_name, class_thresh, output_class, **kw):
    inputs = [hdfs_predictions_input]
    if isinstance(hdfs_input, list):
        inputs += hdfs_input
    else:
        inputs.append(hdfs_input)
    hadoopy.launch_frozen(inputs, hdfs_output, 'thresh_predictions.py',
                          cmdenvs=['CLASSIFIER_NAME=%s' % class_name,
                                   'CLASSIFIER_THRESH=%f' % class_thresh,
                                   'OUTPUT_CLASS=%d' % output_class])


def run_video_keyframe(hdfs_input, hdfs_output, min_resolution, max_resolution, ffmpeg, **kw):
    if not ffmpeg:
        hadoopy.launch_frozen(hdfs_input, hdfs_output, 'video_keyframe.py',
                              reducer=None,
                              cmdenvs=['MIN_RESOLUTION=%d' % min_resolution,
                                       'MAX_RESOLUTION=%f' % max_resolution])
    else:
        with vidfeat.freeze_ffmpeg() as f:
            hadoopy.launch_frozen(hdfs_input, hdfs_output, 'video_keyframe.py',
                                  reducer=None,
                                  cmdenvs=['MIN_RESOLUTION=%d' % min_resolution,
                                           'MAX_RESOLUTION=%f' % max_resolution],
                                  files=f,
                                  jobconfs=['mapred.child.java.opts=-Xmx512M'])


def report_clusters(hdfs_input, local_json_output, sample, category, **kw):
    """
    NOTE: This transfers much more image data than is necessary! Really this operation
    should be done directly on hdfs
    """
    def make_face_image(facestr):
        name, ext = os.path.splitext(facestr)
        m = re.match('(\w+)-face-x(\d+)-y(\d+)-w(\d+)-h(\d+)', name)
        hash, l, t, w, h = m.groups()
        #m = re.match('(\w+)-face-x0(\d+)-y0(\d+)-x1(\d+)-y1(\d+)', name)
        #hash, l, t, r, b = m.groups()
        return {
            'hash': hash,
            'categories': ['faces'],
            'faces': [{'boundingbox': ((l,t),(w,h))}],
            'video': [],
        }

    # Collect all the clusters as a set of lists
    clusters = {}
    count = 0
    for cluster_index, (image_name, _)  in hadoopy.readtb(hdfs_input):
        count += 1
        if count % 100 == 0: print count
        cluster = clusters.setdefault(cluster_index, [])
        if category == 'faces':
            face_image = make_face_image(image_name)
            cluster.append(face_image)
        else:
            cluster.append({
                'hash': image_name,
                'categories': [category],
                'faces': [],
                'video': [],
                })

    # Gather each cluster
    print len(clusters), 'clusters'
    clusters = [{
        # Sample images uniformly
        'sample_images': random.sample(image_set, min(len(image_set), sample)),
        'all_images': image_set,
        'size': len(image_set),
        'children': [],
        'std': 0.0,
        'position': [0.0, 0.0],
        } for image_set in clusters.values()]

    try:
        os.makedirs(os.path.dirname(local_json_output))
    except OSError:
        pass
    report = {category: clusters}
    file_parse.dump(report, local_json_output)


def report_thumbnails(hdfs_input, local_thumb_output, **kw):
    """Collect thumbnails of all images in hdfs://${hdfs_input}
    """
    try:
        os.makedirs(os.path.dirname(local_thumb_output))
    except OSError:
        pass
    count = 0
    for image_hash, image_data in hadoopy.readtb(hdfs_input):
        s = StringIO.StringIO()
        s.write(image_data)
        s.seek(0)
        frame = Image.open(s)
        frame.thumbnail((100,100))
        count += 1
        if count % 100 == 0: print count
        # Sometimes this is a png with an alpha layer
        # TODO: autodetect it?
        frame = frame.convert('RGB')
        path = '%s/%s.jpg' % (local_thumb_output, image_hash)
        frame.save(path)


def report_video_keyframe(hdfs_input, local_json_output, local_thumb_output, **kw):
    videos = {}
    for (kind, hash), v in hadoopy.readtb(hdfs_input):
        if kind == 'frame' and local_thumb_output is not None:
            s = StringIO.StringIO()
            s.write(v)
            s.seek(0)
            frame = Image.open(s)
            try:
                os.makedirs(local_thumb_output)
            except OSError:
                pass
            frame.save(os.path.join(local_thumb_output, '%s.jpg' % hash))
        if kind == 'video':
            videos[hash] = v

    try:
        os.makedirs(os.path.dirname(local_json_output))
    except OSError:
        pass
    report = {'videos': videos}
    file_parse.dump(report, local_json_output)


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

    # Join Predictions with Classifier
    sp = sps.add_parser('join_predictions', help='Joint predictions with images')
    sp.add_argument('hdfs_predictions_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('hdfs_input', nargs='+', **ca['input'])
    sp.add_argument('--local_image_output', help='Path to store local images', default='')
    sp.set_defaults(func=run_join_predictions)

    # Face Finder
    sp = sps.add_parser('face_finder', help='Extract faces')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('--image_length', **ca['image_length'])
    sp.add_argument('--boxes', help='If True make the value (image_data, boxes) where boxes is a list of (x, y, h, w)', type=bool, default=False)
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

    # Run Video Keyframing
    sp = sps.add_parser('video_keyframe', help='Run Video Keyframing')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('hdfs_output', **ca['output'])
    sp.add_argument('min_resolution', type=int, help='Maximum number of keyframes in each cluster')
    sp.add_argument('max_resolution', type=float, help='Minimum number seconds between keyframes')
    sp.add_argument('--ffmpeg', help='Use frozen ffmpeg binary instead of pyffmpeg (works with more kinds of encoded videos, poorly enocded videos)', action='store_true')
    sp.set_defaults(func=run_video_keyframe)

    # Visualize Clusters
    sp = sps.add_parser('visualize', help='Visualize clusters')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.set_defaults(func=run_visualize)

    # Report Categories from Prediction Output
    sp = sps.add_parser('report_categories', help='Report Categories from Prediction Output')
    sp.add_argument('hdfs_join_predictions_input', **ca['input'])
    sp.add_argument('local_output', help='report output')
    sp.add_argument('--image_limit', help='fill each category with <image_limit> highest confidences',
                    type=int, default=200)
    sp.add_argument('--local_thumb_output', help='folder of image thumbnails', default=None)
    sp.set_defaults(func=report_categories)

    # Report Clustering
    sp = sps.add_parser('report_clusters', help='Report Clusters')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('local_json_output', help='report output')
    sp.add_argument('category', help='category tag for this clustering')
    sp.add_argument('--sample', help='sample size', type=int, default=20)
    sp.set_defaults(func=report_clusters)

    # Report Video Keyframes
    sp = sps.add_parser('report_video_keyframe', help='Report Video Keyframes')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('local_json_output', help='report output')
    sp.add_argument('--local_thumb_output', help='local thumbnail output directory')
    sp.set_defaults(func=report_video_keyframe)

    # Local Thumbnail Output
    sp = sps.add_parser('report_thumbnails', help='Report Categories from Face Clustering')
    sp.add_argument('hdfs_input', **ca['input'])
    sp.add_argument('local_thumb_output', help='local thumbnail output directory')
    sp.set_defaults(func=report_thumbnails)

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()
