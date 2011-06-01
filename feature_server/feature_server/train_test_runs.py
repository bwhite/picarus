import classipy
import imfeat
import random
import Image
import json
import itertools
import re
import cPickle as pickle

from feature_server import cass

# Have a list of features to evaluate and compare
feature_strs = cass.get_available_features()
"""
feature_str = [
    "imfeat.Moments(mode='rgb', 2)",
    "imfeat.Moments(mode='rgb', 2)",    
    "imfeat.GIST()",
]
"""

cf_labels = cass.pycassa.ColumnFamily(cass.pool, 'amiller_sun09label')
cf_runs = cass.pycassa.ColumnFamily(cass.pool, 'amiller_testruns')


def build_label_index(buffer_size=1000):
    # Get label
    def reverse(items):
        for k, v in items:
            d = json.loads(v)
            g = re.match('(\w+)-(?:\d+)\.jpg', d['filename'])
            if g: yield g.groups()[0], {k:''}

    items = cass.buffered_get_row(cass.cf_images, 'image_metadata')
    items = reverse(items)

    # Insert into cass by chunks
    count = 0
    while items:
        chunk = list(itertools.islice(items, buffer_size))
        for row, column in chunk:
            cf_labels.insert(row, column)
        count += len(chunk)
        if not chunk: break

    print("Built index with %d items" % count)


def get_label_index():
    columns = cf_labels.get_range(column_count=10000)
    return columns


def train_classifier(label_values_=None):
    """Trains the classifier
    Args:
        label_values_: if None (default) uses the current global value
    Modified state:
        classifier: is now trained
    """
    # Use a simple linear SVM classifier without any special parameters
    global classifier
    classifier = classipy.SVMLinear()

    if label_values_ is None:
        label_values_ = label_values

    classifier.train(label_values_)

    with open('classifier.pkl','w') as f:
        f.write(classifier.dumps())

    return classifier


def train_and_test(classifier_class, label_values):
    pass


def train_sample(feature_str, label, pos_train=0.5, neg_train=1000):
    """Perform training and testing using disjont samples from the full
    set of label_values. This is equivalent to doing one round of cross
    validation (see classipy.cross_validation) only it keeps the values around
    for display.

    Args:

    """
    all_hashes = list(cass.get_image_hashes())
    pos_hashes = [_[0] for _ in cass.buffered_get_row(cf_labels, label)]
    neg_hashes = list(set(all_hashes) - set(pos_hashes))

    if 0 < pos_train <= 1: pos_train = int(pos_train * len(pos_hashes))
    if 0 < neg_train <= 1: neg_train = int(neg_train * len(neg_hashes))

    # Choose a training sample and a testing sample
    if len(pos_hashes) < pos_train:
        raise ValueError('Not enough positive examples %s(%d)' % \
                         (label, len(pos_hashes)))
    if len(neg_hashes) < neg_train:
        raise ValueError('Not enough negative examples %s(%d)' % \
                         (label, len(neg_hashes)))

    pos_sample = random.sample(pos_hashes, pos_train)
    neg_sample = random.sample(neg_hashes, neg_train)

    labels = [-1 for _ in neg_sample] + [1 for _ in pos_sample]
    values = cass.get_feature_values(feature_str, neg_sample+pos_sample)

    global label_values
    label_values = zip(labels, values)

    print 'Training classifier with sample %d' % len(label_values)
    train_classifier(label_values)


def split_train_test(label, pos_train=0.5, neg_train=1000):
    """Splits the data into a training and testing sample.
    Arguments:
       pos_train:
          0 < pos_train <= 1.0: the portion of the set to use for training
          1 < pos_train: the number of images to use for training

    Returns:
       (train, test): Training and testing set, where

          train: Iterable of tuples for a training set
             [(-1|1, hash), ...]

          test: Iterable of tuples for a testing set
             [(-1|1, hash), ...]
    """
    all_hashes = set(cass.get_image_hashes())
    pos_hashes = [_[0] for _ in cass.buffered_get_row(cf_labels, label)]
    neg_hashes = set(all_hashes) - set(pos_hashes)

    if 0 < pos_train <= 1:
        pos_train = int(pos_train * len(pos_hashes))
    if 0 < neg_train <= 1:
        neg_train = int(neg_train * len(neg_hashes))

    pos_sample = random.sample(pos_hashes, pos_train)
    neg_sample = random.sample(neg_hashes, neg_train)

    # Sample from pos and neg
    train = [(-1, k) for k in neg_sample] + \
            [(1, k) for k in pos_sample]

    neg_sample = random.sample(neg_hashes, len(pos_hashes))

    # Use all of the images for testing for now
    test = [(-1, k) for k in neg_sample] + \
           [(1, k) for k in pos_hashes]

    print 'Train: %d   Test: %d' % (len(train), len(test))

    return train, test


def run_train_test(feature_str, label, split_opts={}):
    """
    Args:
        split_opts: passed to split_train_test
    Returns:
        (label, [(conf, gt, hash), ...]
        where
            label: string label, e.g. 'airplane'
            conf: -inf to inf, prediction confidence
            gt: -1 or 1 for negative or positive annotation
            hash: image key for use with cass.get_image
    """

    train, test = split_train_test(label, **split_opts)

    # Train
    labels = (L for L, k in train)
    hashes = [k for L, k in train]
    values = cass.get_feature_values(feature_str, hashes)
    label_values = zip(labels, values)

    print 'Training classifier with %d values' % len(label_values)
    classifier = train_classifier(label_values)

    # Test
    hashes = [k for L, k in test]
    values = list(cass.get_feature_values(feature_str, hashes))
    print('Testing with %d(%d) values' % (len(hashes),len(values)))
    conf_label = (classifier.predict(value) for value in values)

    conf_gt_hash = [(pred*conf, L, k)
                    for ((pred, conf),), (L, k)
                    in zip(conf_label, test)]
    conf_gt_hash = sorted(conf_gt_hash, key=lambda _: _[0])    

    return (label, conf_gt_hash)


def run_all_train_test(feature_str, labels=None):
    if labels is None:
        labels = [_[0] for _ in cf_labels.get_range(column_count=1)]

    results = [run_train_test(feature_str, label)
                    for label in labels]

    cf_runs.insert('test', {'run_items': pickle.dumps(results, -1)})


def get_run(run_key):
    run = cf_runs.get(run_key, ['run_items'])['run_items']
    return pickle.loads(run)


def get_available_runs():
    return [_[0] for _ in cf_runs.get_range(column_count=1)]


if __name__ == "__main__":
    pass
