import hadoopy
from picarus import _file_parse as file_parse
import glob
import os
import tempfile
import picarus


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def _parser(sps):
    import picarus.__main__
    ca = picarus.__main__._ca
    # Make labels pkl
    s = sps.add_parser('classifier_labels', help='Given positive/negative inputs, make/update the labels .pkl for training the classifier')
    s.add_argument('hdfs_input_pos', **ca['input'])
    s.add_argument('hdfs_input_neg', **ca['input'])
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('classifier_name', help='Name to give the classifier (e.g., indoor_outdoor).  This is used by the classifier training.')
    s.add_argument('local_labels', help='Path to labels file, this can be an existing file and any existing classifier_name entry is replaced.')
    s.add_argument('--classifier', help='Classifier to use from classifiers.py (default: svmlinear)', default='svmlinear')
    s.add_argument('--classifier_extra', help='Additional data to pass to classifier (e.g., parameters). (default: '')', default='')
    s.set_defaults(func=picarus.classify.run_classifier_labels)

    # Train Classifier (take in features from the previous labeling step)
    s = sps.add_parser('train_classifier', help='Train classifier on feature vectors')
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('local_labels', help='Path to labels file, this can be an existing file and any existing classifier_name entry is replaced.')
    s.add_argument('hdfs_input', nargs='+', **ca['input'])
    s.set_defaults(func=picarus.classify.run_train_classifier)

    # Predict Classifier
    s = sps.add_parser('predict_classifier', help='Predict classifier on feature vectors')
    s.add_argument('hdfs_classifier_input', **ca['input'])
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('hdfs_input', nargs='+', **ca['input'])
    s.set_defaults(func=picarus.classify.run_predict_classifier)

    # Join Predictions with Classifier
    s = sps.add_parser('join_predictions', help='Joint predictions with images')
    s.add_argument('hdfs_predictions_input', **ca['input'])
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('hdfs_input', nargs='+', **ca['input'])
    s.add_argument('--local_image_output', help='Path to store local images', default='')
    s.set_defaults(func=picarus.classify.run_join_predictions)


def run_classifier_labels(hdfs_input_pos, hdfs_input_neg, hdfs_output, classifier_name, classifier_extra, local_labels, classifier, **kw):
    """
    TODO Finish docstring
    Args:
        hdfs_output: Path to hdfs temporary output or None if execution should be performed locally using hadoopy.launch_local.
    """
    labels = {}
    try:
        labels = file_parse.load(local_labels)
    except IOError:
        pass
    if hdfs_output is None:
        j = hadoopy.launch_local(hdfs_input_pos, None, _lf('collect_keys.py'))
        pos_keys = sum((x[1] for x in j['output']), [])
        j = hadoopy.launch_local(hdfs_input_neg, None, _lf('collect_keys.py'))
        neg_keys = sum((x[1] for x in j['output']), [])
    else:
        hdfs_output_pos = hdfs_output + '/pos'
        hdfs_output_neg = hdfs_output + '/neg'
        picarus._launch_frozen(hdfs_input_pos, hdfs_output_pos, _lf('collect_keys.py'))
        picarus._launch_frozen(hdfs_input_neg, hdfs_output_neg, _lf('collect_keys.py'))
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
    picarus._launch_frozen(hdfs_input, hdfs_output, _lf('train_classifier.py'),
                           files=files,
                           cmdenvs=['LOCAL_LABELS_FN=%s' % os.path.basename(local_labels)],
                           jobconfs_default=['mapred.task.timeout=6000000'],
                           **kw)


def run_predict_classifier(hdfs_input, hdfs_classifier_input, hdfs_output, classes=None, image_hashes=None, **kw):
    import classipy
    # NOTE: Adds necessary files
    files = glob.glob(classipy.__path__[0] + "/lib/*")
    fp = tempfile.NamedTemporaryFile(suffix='.pkl.gz')
    file_parse.dump([x for x in hadoopy.readtb(hdfs_classifier_input)
                     if classes is None or x[0] in classes], fp.name)
    files.append(fp.name)
    picarus._launch_frozen(hdfs_input, hdfs_output, _lf('predict_classifier.py'),
                           files=files, reducer=None,
                           cmdenvs=['CLASSIFIERS_FN=%s' % os.path.basename(fp.name)],
                           image_hashes=image_hashes,
                           dummy_arg=fp)


def run_join_predictions(hdfs_predictions_input, hdfs_input, hdfs_output, local_image_output, **kw):
    inputs = [hdfs_predictions_input]
    if isinstance(hdfs_input, list):
        inputs += hdfs_input
    else:
        inputs.append(hdfs_input)
    picarus._launch_frozen(inputs, hdfs_output, _lf('join_predictions.py'))
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


def run_thresh_predictions(hdfs_predictions_input, hdfs_input, hdfs_output, class_name, class_thresh, output_class, in_memory=False, **kw):
    inputs = [hdfs_predictions_input]
    if isinstance(hdfs_input, list):
        inputs += hdfs_input
    else:
        inputs.append(hdfs_input)
    launcher = hadoopy.launch_local if in_memory else picarus._launch_frozen
    launcher(inputs, hdfs_output, _lf('thresh_predictions.py'),
             cmdenvs=['CLASSIFIER_NAME=%s' % class_name,
                      'CLASSIFIER_THRESH=%f' % class_thresh,
                      'OUTPUT_CLASS=%d' % output_class],
             num_reducers=1)


def thresh_predictions(hdfs_predictions_input, class_name, class_thresh):
    """
    Args:
        hdfs_predictions_input:  HDFS in the form of (image_hash, predictions)
        class_name: Class name for predictions
        class_thresh: Positive if thresh <= conf

    Returns:
        (neg_image_hashes, pos_image_hashes) where each is a set
    """
    hash_label_confs = ((image_hash, predictions[class_name][0][0], predictions[class_name][0][1])
                        for image_hash, predictions in hadoopy.readtb(hdfs_predictions_input))
    hash_pols = [(image_hash, class_thresh <= label * conf) for image_hash, label, conf in hash_label_confs]
    pos_image_hashes = set(image_hash for image_hash, pol in  hash_pols if pol)
    neg_image_hashes = set(image_hash for image_hash, pol in  hash_pols if not pol)
    return neg_image_hashes, pos_image_hashes
