#!/usr/bin/env python
# (C) Copyright 2011 Dapper Vision, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Vlad I. Morariu <morariu@umd.edu>'
__license__ = 'GPL V3'

import time
import hadoopy
import os
import cPickle as pickle
import cv
import imfeat
import glob
import tempfile
import picarus
# need this to load the pickle file of the Eigenfaces feature
from picarus.vision import face_feature


def _compute_exemplar_feature(exemplar_fn, feature_pkl, fp):
    im = cv.LoadImage(exemplar_fn)
    fixed_size = cv.CreateImage((64, 64), 8, im.channels)
    cv.Resize(im, fixed_size, cv.CV_INTER_LINEAR)
    feat = pickle.load(open(feature_pkl, 'rb'))
    pickle.dump(imfeat.compute(feat, fixed_size)[0], fp)


def run_face_ranker(hdfs_input, hdfs_output,
                    feature_pkl, exemplar_fn):
    """
    Runs the face_ranker.py hadoopy script.  The output consists of
    the distance of each image to an exemplar as key, and the
    input tuple of (key, imagedata) as value.
    Inputs:
    - hdfs_input: path to hdfs input: (key, imagedata) pairs
    - hdfs_output: path to the hdfs output tuples: (dist, (key, imagedata))
      where dist is the distance in Eigenfaces feature space to the exemplar
      image
    - feature_pkl: pickle file containing a trained Eigenfaces feature
    - exemplar_fn: filename of the exemplar image
    """
    fp = tempfile.NamedTemporaryFile()
    _compute_exemplar_feature(exemplar_fn, feature_pkl, fp)
    fp.flush()
    hadoopy.launch_frozen(hdfs_input, hdfs_output,
                          'face_ranker.py',
                          cmdenvs=['EXEMPLAR_FN=%s' % os.path.basename(fp.name),
                                   'FEATURE_FN=%s' % os.path.basename(feature_pkl)],
                          files=[feature_pkl, fp.name])


# all functions below are for setting up inputs and testing run_face_ranker()
def _train_feature(feature_pkl):
    """train and save an eigenfaces feature if it does not already exist"""
    if not os.path.exists(feature_pkl):
        print('Training eigenfaces feature (%s)...' % feature_pkl)
        import eigenfaces_train
        training_fns = eigenfaces_train.get_unique_lfw_training_images()
        eigenfaces_train.train(training_fns, feature_pkl)


def _load_input_data(data_fn):
    """copy fddb data to hdfs if it is not already there"""
    if not hadoopy.exists(data_fn):
        print('Creating input data \'%s\'...' % data_fn)
        import fddb_data
        fddb_data.write_tb(data_fn)


def _visualize_results(exemplar_path):
    viz_dir = 'out_face_ranker_ims'
    if not os.path.exists(viz_dir):
        os.makedirs(viz_dir)
    for f in glob.glob('%s/*.jpg' % viz_dir):
        os.remove(f)
    keys = [(k1, k2) for k1, (k2, v) in pickle.load(open('out_face_ranker.pkl', 'r'))]
    dist_map = dict([(k2, i) for i, (k1, k2) in enumerate(sorted(keys))])
    for dist, (imname, imdata) in pickle.load(open('out_face_ranker.pkl', 'r')):
        with open('%s/%08i_%0.4f.jpg' % (viz_dir, dist_map[imname], dist), 'w') as fp:
            fp.write(imdata)
    im = cv.LoadImage(exemplar_path)
    cv.SaveImage('%s/%08i_0.0000_exemplar.jpg' % (viz_dir, 0), im)


def _download_outputs(out_path):
    with open('out_face_finder.pkl', 'w') as f:
        pickle.dump(list(hadoopy.readtb(out_path + 'out_face_finder')), f)
    with open('out_face_ranker.pkl', 'w') as f:
        pickle.dump(list(hadoopy.readtb(out_path + 'out_face_ranker')), f)


def test_face_ranker():
    """
    Set up input data, run face_finder on it, and then use the output of
    face_finder as input to the face_ranker.  Finally download the
    results for visualization.
    """
    cur_time = time.time()
    data_fn = 'fddb_test_data/all_folds.tb'
    out_path = 'face_feature_out/%f/' % cur_time
    side_path = 'data/'
    feature_pkl = side_path + 'eigenfaces_flickr.pkl'
    exemplar_path = side_path + 'exemplar2.jpg'
    os.makedirs(out_path)
    if not os.path.exists(side_path):
        os.makedirs(side_path)
    # intermediate and final results
    ranker_in_path = out_path + 'out_face_finder'
    ranker_out_path = out_path + 'out_face_ranker'
    # set up the input to face ranker
    _train_feature(feature_pkl)
    _load_input_data(data_fn)
    picarus.vision.run_face_finder(data_fn, ranker_in_path,
                                   image_length=64, boxes=False)
    # the main face ranker call
    run_face_ranker(ranker_in_path, ranker_out_path, feature_pkl, exemplar_path)
    # download the results for visualization
    _download_outputs(out_path)
    _visualize_results(exemplar_path)


def main():
    test_face_ranker()


if __name__ == '__main__':
    main()
