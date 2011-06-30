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
"""Test
"""
__author__ = 'Vlad I. Morariu <morariu@umd.edu>'
__license__ = 'GPL V3'


from picarus.vision import face_feature
import imfeat
import cv
import lfwcrop_data
import numpy as np
import random
try:
    import unittest2 as unittest
except ImportError:
    import unittest


def get_lfw_restricted_accuracy(split):
    max_train_ims = 3000
    train_data = lfwcrop_data.get_lfw_cropped_data('%s_train' % split, 'data')
    test_data = lfwcrop_data.get_lfw_cropped_data('%s_test' % split, 'data')

    # get a list of unique training images
    train_fns = []
    for fnpair in train_data.keys():
        train_fns.extend(fnpair)
    train_fns = sorted(set(train_fns))

    # load the unique training images, and learn PCA
    print('Training Eigenfaces feature space (%i training images)...' % (
          len(train_fns)))
    if len(train_fns) <= max_train_ims:
        train_ims = map(cv.LoadImage, train_fns)
    else:
        train_ims = map(cv.LoadImage, random.sample(train_fns, max_train_ims))
    feat = face_feature.Eigenfaces(train_ims)

    # go through each training image pair and calculate distances
    dists = []
    classmap = {'same' : 1, 'diff' : 0}
    for ((fn1, fn2), attr) in train_data.items():
        #print('Calculating distance between (%s, %s)' % (
        #    os.path.basename(fn1), os.path.basename(fn2)))
        f1 = imfeat.compute(feat, cv.LoadImage(fn1))[0]
        f2 = imfeat.compute(feat, cv.LoadImage(fn2))[0]
        dists.append((np.linalg.norm(f1-f2), classmap[attr['class']]))

    # calculate threshold that maximizes average accuracy
    dists = sorted(dists)
    p = len(filter(lambda x: x[1] == 0, dists))
    n = len(filter(lambda x: x[1] == 1, dists))
    tpi, tni = 0, n
    a = []
    for (d, v) in dists:
        if v == 1:
            tpi += 1
        else:
            tni -= 1
        a.append((tpi + tni) / float(p + n))
    imax = np.argmax(np.array(a))
    thresh = dists[imax][0]
    print('Thresh %4.3g yields a classification accuracy of %4.3g' % (
        thresh, a[imax]))

    # now test on testing split
    right = 0
    for ((fn1, fn2), attr) in test_data.items():
        #print('Calculating distance between (%s, %s)' % (
        #    os.path.basename(fn1), os.path.basename(fn2)))
        f1 = imfeat.compute(feat, cv.LoadImage(fn1))[0]
        f2 = imfeat.compute(feat, cv.LoadImage(fn2))[0]
        d = np.linalg.norm(f1-f2)
        if(d <= thresh and attr['class'] == 'same' or
           d > thresh and attr['class'] == 'diff'):
            right += 1
    accuracy = float(right) / len(test_data)
    print('Testing accuracy %4.3g' % accuracy)
    return accuracy


class Test(unittest.TestCase):

    def test_0(self):
        accuracies = map(get_lfw_restricted_accuracy,
                         map(lambda x: '%02i' % x, range(1, 11)))
        accuracy_avg = np.mean(np.array(accuracies))
        accuracy_std = np.std(np.array(accuracies))
        print('Accuracy on LFW test set (10 fold CV): %4.3g +/- %4.3g' % (
            accuracy_avg, accuracy_std))


if __name__ == '__main__':
    unittest.main()
    #get_lfw_restricted_accuracy('dv')
