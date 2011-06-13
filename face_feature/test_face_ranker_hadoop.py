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
import unittest
import hadoopy
import os
# not used here, but needed so that it is packaged along in launch_frozen
import face_feature


class TestFaceRankerHadoop(unittest.TestCase):

    def __init__(self, *args, **kw):
        super(TestFaceRankerHadoop, self).__init__(*args, **kw)
        cur_time = time.time()
        self.data_fn = 'fddb_test_data/fold_01.tb'
        self.out_path = 'face_feature_out/%f/' % cur_time
        self.side_path = 'side/'
        self.eigenfaces_fn = self.side_path + 'eigenfaces_lfw_cropped.pkl'
        os.makedirs(self.out_path)
        if not os.path.exists(self.side_path):
            os.makedirs(self.side_path)
        #self.launcher = hadoopy.launch_local
        self.launcher = hadoopy.launch_frozen

    def _train_feature(self):
        # train and save an eigenfaces feature if it does not already exist
        if not os.path.exists(self.eigenfaces_fn):
            print('Training eigenfaces feature (%s)...' % self.eigenfaces_fn)
            import eigenfaces_train
            training_fns = eigenfaces_train.get_unique_lfw_training_images()
            eigenfaces_train.train(training_fns, self.eigenfaces_fn)

    def _load_input_data(self):
        # copy fddb data to hdfs if it is not already there
        if not hadoopy.exists(self.data_fn):
            print('Creating input data \'%s\'...' % self.data_fn)
            import fddb_data
            fddb_data.write_tb(self.data_fn, 1)

    def _run_face_finder(self):
        in_path = self.data_fn
        out_path = self.out_path + 'out_face_finder'
        self.launcher(in_path, out_path,
                      '../image_clustering/face_finder.py', reducer=False,
                      files=['../../hadoopy/tests/haarcascade_frontalface_default.xml'])

    def _run_face_ranker(self):
        in_path = self.out_path + 'out_face_finder'
        out_path = self.out_path + 'out_face_ranker'
        self.launcher(in_path, out_path,
                      'face_ranker.py',
                      files=[self.eigenfaces_fn])

    def test_setup(self):
        self._train_feature()
        self._load_input_data()
        self._run_face_finder()
        self._run_face_ranker()
        import cPickle
        with open('out_face_finder.pkl', 'w') as f:
            cPickle.dump(list(hadoopy.readtb(self.out_path + 'out_face_finder')), f)
        with open('out_face_ranker.pkl', 'w') as f:
            cPickle.dump(list(hadoopy.readtb(self.out_path + 'out_face_ranker')), f)


if __name__ == '__main__':
    unittest.main()
