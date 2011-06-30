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
"""
Train an Eigenface feature on the lfw dataset.
"""
__author__ = 'Vlad I. Morariu <morariu@umd.edu>'
__license__ = 'GPL V3'


from picarus.vision import face_feature
import cv
import random
import cPickle
import glob
import sys


def get_flickr_training_images():
    return glob.glob('faces_cropped/*.jpg')


def resize_im(im, size):
    if not cv.GetSize(im) == size:
        im_resized = cv.CreateImage(size, im.depth, im.nChannels)
        cv.Resize(im, im_resized, cv.INTER_LINEAR)
        im = im_resized
    return im


def train(training_fns, pickle_fn, max_train_ims=3000, size=(64, 64)):
    # load the unique training images, and learn PCA
    print('Training Eigenfaces feature space (%i training images)...' % (
          len(training_fns)))
    if len(training_fns) <= max_train_ims:
        train_ims = [resize_im(cv.LoadImage(fn, 1), size) for fn in training_fns]
    else:
        train_ims = [resize_im(cv.LoadImage(fn, 1), size)
                     for fn in  random.sample(training_fns, max_train_ims)]
    feat = face_feature.Eigenfaces(train_ims)
    with open(pickle_fn, 'w') as fp:
        cPickle.dump(feat, fp)


if __name__ == '__main__':
    if(len(sys.argv) > 1 and sys.argv[1] == 'flickr'):
        pickle_fn = 'data/eigenfaces_flickr.pkl'
        training_fns = get_flickr_training_images()
    else:
        import lfwcrop_data
        pickle_fn = 'data/eigenfaces_lfw_cropped.pkl'
        training_fns = lfwcrop_data.get_unique_lfw_training_images('data')
    train(training_fns, pickle_fn)
