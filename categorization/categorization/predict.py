import classipy
import imfeat
import random
import Image
import json
import itertools
import re

from feature_server import cass

# Use a simple linear SVM classifier without any special parameters
if not 'classifier' in globals():
    classifier = classipy.SVMLinear()

# Have a list of features to evaluate and compare
feature_strs = [
    "imfeat.Moments(mode='rgb', 2)",
    "imfeat.GIST()",
]

# Dataset (parallel arrays)
hashes_filenames = None

# Intermetediate feature results
label_values = None


def build_label_index(buffer_size=1000):
    cf_labels = cass.pycassa.ColumnFamily(cass.pool, 'amiller_sun09label')

    # Group the iterator by chunks
    def grouper(n, iterable):
        args = [iter(iterable)] * n
        return itertools.izip_longest(*args)

    # Get label
    def reverse(items):
        for k, v in items:
            d = json.loads(v)
            if not 'filename' in d: continue
            g = re.match('(\w+)-(?:\d+)\.jpg', d['filename'])
            if g: yield g.groups()[0], k

    items = cass.buffered_get_row(cass.cf_images, 'image_metadata')
    items = reverse(items)

    # Insert into cass by chunks
    count = 0
    while items:
        d = dict(itertools.islice(items, buffer_size))
        cf_labels.insert('amiller_sun09label', columns=d)
        count += len(d)

    print("Built index with %d items" % count)


def train_classifier(label_values_=None):
    """Trains the classifier
    Args:
        label_values_: if None (default) uses the current global value
    Modified state:
        classifier: is now trained
    """
    if label_values_ is None:
        label_values_ = label_values

    classifier.train(label_values_)

    with open('classifier.pkl','w') as f:
        f.write(classifier.dumps())


def train_sample(feature, train=1, train_n=None):
    """Perform training and testing using disjont samples from the full
    set of label_values. This is equivalent to doing one round of cross
    validation (see classipy.cross_validation) only it keeps the values around
    for display.

    Args:

    """
    hash_name_labels = cass.get_hashes_filenames()

    # Choose a training sample and a testing sample
    train_n = int(len(hash_name_labels) * train) if train_n is None else train_n

    train_sample = random.sample(hash_name_labels, train_n)

    global label_values
    label_values = zip([int(label=='documents') for _, _, label in train_sample],
                       cass.get_feature_value(feature,
                                              [im_hash for im_hash,_,_
                                               in train_sample]))

    print 'Training classifier with sample %d' % len(label_values)
    train_classifier(label_values)


def test_sample(feature, test=1, test_n=None):
    hash_name_labels = cass.get_hashes_filenames()
    test_n = int(len(hash_name_labels) * test) if test_n is None else test_n
    test_sample = random.sample(hash_name_labels, test_n)
    values = cass.get_feature_value(feature,
                                    [im_hash for im_hash,_,_
                                     in test_sample])

    # Initialize the [(conf, image)] lists for each class
    global class_conf
    class_conf = []
    for (h, name, gt), value in zip(hash_name_labels, values):
        (conf, label), = classifier.predict(value)
        conf = conf if label == 0 else -conf
        class_conf.append((conf, h, gt))


if __name__ == "__main__":
    pass
