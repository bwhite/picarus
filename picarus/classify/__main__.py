import hadoopy
from picarus import _file_parse as file_parse
import glob
import os
import tempfile


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def run_classifier_labels(hdfs_input_pos, hdfs_input_neg, hdfs_output, classifier_name, classifier_extra, local_labels, classifier, **kw):
    labels = {}
    try:
        labels = file_parse.load(local_labels)
    except IOError:
        pass
    hdfs_output_pos = hdfs_output + '/pos'
    hdfs_output_neg = hdfs_output + '/neg'
    hadoopy.launch_frozen(hdfs_input_pos, hdfs_output_pos, _lf('collect_keys.py'))
    hadoopy.launch_frozen(hdfs_input_neg, hdfs_output_neg, _lf('collect_keys.py'))
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
    hadoopy.launch_frozen(hdfs_input, hdfs_output, _lf('train_classifier.py'),
                          files=files,
                          cmdenvs=['LOCAL_LABELS_FN=%s' % os.path.basename(local_labels)])


def run_predict_classifier(hdfs_input, hdfs_classifier_input, hdfs_output, **kw):
    import classipy
    # NOTE: Adds necessary files
    files = glob.glob(classipy.__path__[0] + "/lib/*")
    fp = tempfile.NamedTemporaryFile(suffix='.pkl.gz')
    file_parse.dump(list(hadoopy.readtb(hdfs_classifier_input)), fp.name)
    files.append(fp.name)
    hadoopy.launch_frozen(hdfs_input, hdfs_output, _lf('predict_classifier.py'),
                          files=files, reducer=None,
                          cmdenvs=['CLASSIFIERS_FN=%s' % os.path.basename(fp.name)],
                          dummy_arg=fp)


def run_join_predictions(hdfs_predictions_input, hdfs_input, hdfs_output, local_image_output, **kw):
    inputs = [hdfs_predictions_input]
    if isinstance(hdfs_input, list):
        inputs += hdfs_input
    else:
        inputs.append(hdfs_input)
    hadoopy.launch_frozen(inputs, hdfs_output, _lf('join_predictions.py'))
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
    hadoopy.launch_frozen(inputs, hdfs_output, _lf('thresh_predictions.py'),
                          cmdenvs=['CLASSIFIER_NAME=%s' % class_name,
                                   'CLASSIFIER_THRESH=%f' % class_thresh,
                                   'OUTPUT_CLASS=%d' % output_class])
