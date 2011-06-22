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

"""Code for training OpenCV face detector."""

__author__ = 'Vlad I. Morariu <morariu@umd.edu>'
__license__ = 'GPL V3'

import hadoopy
import Image
import imfeat
import cStringIO as StringIO
import cv
import numpy as np
import os
import glob
import subprocess


def get_existing_paths(path_pos, path_neither, path_neg):
    """
    Just in case some files have already been moved to the positive or
    negative folders, construct a dictionary mapping a key to
    one of the paths (save_display_images will use the 'neither' directory
    if an image's hash is not found).
    """
    key_to_path = {}
    for d in [path_pos, path_neither, path_neg]:
        if not os.path.exists(d):
            os.makedirs(d)
        key_to_path.update([(os.path.splitext(
            os.path.basename(f))[0], d) for f in glob.glob('%s/*' % d)])
    return key_to_path


def save_display_images(path_hdfs, path_local, max_count, key_to_path=None):
    """
    Saves the first max_count images obtained by calling
    hadoopy.readtb(path_hdfs).  Each item in the sequence is assumed
    to be of the form (key, (imagedata, boxes)).  The boxes are
    drawn on each image before it is saved to the local path.
    If key_to_path is provided, which maps a key to a path, the image
    corresponding to that key will be saved in key_to_path[key].
    """
    if key_to_path == None:
        key_to_path = {}
    count = 0
    for k, (i, bs) in hadoopy.readtb(path_hdfs):
        if k in key_to_path:
            path = key_to_path[k]
        else:
            path = path_local
        filename = '%s/%s.jpg' % (path, k)
        im = imfeat.convert_image(Image.open(StringIO.StringIO(i)),
                                  [('opencv', 'bgr', 8)])
        print(k)
        for b in bs:
            cv.Rectangle(im, (b[0], b[1]), (b[2], b[3]),
                         cv.CV_RGB(255, 0, 0), 3)
        cv.SaveImage(filename, im)
        # update count and break loop if necessary
        # TODO(Vlad): can we slice notation on a list of generators?
        count += 1
        if count > max_count:
            break


def make_training_set(path_hdfs, pos_disp_dir, neg_disp_dir,
                      pos_dir, neg_dir, pos_file, neg_file, max_count):
    """
    Makes a training set by downloading the original images (w/o overlayed
    boxes) corresponding to the positives and negatives from the display
    directories.  The file lists used as input by opencv_createsamples and
    by opencv_haartraining are also created.
    """
    key_to_path = {}
    for (d1, d2) in [(pos_disp_dir, pos_dir), (neg_disp_dir, neg_dir)]:
        if not os.path.exists(d2):
            os.makedirs(d2)
        key_to_path.update([(os.path.splitext(
            os.path.basename(f))[0], d2) for f in glob.glob('%s/*' % d1)])

    pos_fp = open(pos_file, 'w')
    neg_fp = open(neg_file, 'w')

    count = 0
    for k, (i, bs) in hadoopy.readtb(path_hdfs):
        try:
            path = key_to_path[k]
            # save the original image
            filename = '%s/%s.jpg' % (path, k)
            print(filename)
            with open(filename, 'wb') as f:
                f.write(i)
                # update the positive/negative training lists
                if path == pos_dir:
                    pos_fp.write('%s %i' % (filename, len(bs)))
                    for b in bs:
                        pos_fp.write(' %i %i %i %i' % (
                            b[0], b[1], b[2] - b[0] + 1, b[3] - b[1] + 1))
                    pos_fp.write('\n')
                else:
                    neg_fp.write('%s\n' % filename)
        except KeyError:
            pass
        # update count and break loop if necessary
        # TODO(Vlad): can we slice notation on a list of generators?
        count += 1
        if count > max_count:
            break

    pos_fp.close()
    neg_fp.close()


def train_classifier(pos_file, neg_file, out_dir,
                     nneg=3000, npos=7000,
                     nstages=20, nsplits=3,
                     memory=500,
                     minhitrate=.999, maxfalsealarm=.5,
                     size=(20, 20)):
    """
    Trains a object detector using OpenCV's haartraining code.  The default
    values are those described in Intel's tech report on this topic:
    Empirical Analysis of Detection Cascades of Boosted Classifiers for
    Rapid Object Detection, by Rainier Lienhart, Alexander Kuranov, and
    Vadim Pisarevsky.
    See OpenCV's haartraining.htm tutorial for a description of the parameters.
    """
    # create the vec file that will be the input to haartraining
    cmd = 'opencv_createsamples -info %s -vec %s.vec -w %i -h %i' % (
        pos_file, pos_file, size[0], size[1])
    print(cmd)
    subprocess.call(cmd.split())

    # train classifier
    cmd = ('opencv_haartraining -data %s -vec %s.vec -bg %s -nneg %i -npos %i'
           ' -nstages %i -nsplits %i -mem %i -sym'
           ' -minhitrate %g -maxfalsealarm %g -w %i -h %i' % (
        out_dir, pos_file, neg_file, nneg, npos, nstages, nsplits,
        memory, minhitrate, maxfalsealarm, size[0], size[1]))
    print('\n\n%s' % cmd)
    subprocess.call(cmd.split())

    # test classifier on the annotated training set
    cmd = 'opencv_performance -data %s -info %s -w %i -h %i' % (
        out_dir, pos_file, size[0], size[1])
    print('\n\n%s' % cmd)
    subprocess.call(cmd.split())


def main():
    # the paths for storing images in which all faces were detected
    # and where some or no faces were detected
    path_disp_pos = 'faces_disp_pos'
    path_disp_neither = 'faces_disp_neither'
    path_disp_neg = 'faces_disp_neg'
    path_out = 'face_classifier'
    path_hdfs = '/user/root/flickr_hash_faces7'
    path_pos = 'faces_pos'
    path_neg = 'faces_neg'
    pos_file = 'train_pos.txt'
    neg_file = 'train_neg.txt'
    max_count = 1000

    # save paths of images that have already been manually sorted
    key_to_path = get_existing_paths(
        path_disp_pos, path_disp_neither, path_disp_neg)
    # download images from hdfs and place them in the 'neither' directory,
    # unless they have already been moved to some other directory
    #save_display_images(path_hdfs, path_disp_neither, max_count, key_to_path)

    # now manually sort the display images into ones that should be used as
    # positives (those in which all people are detected), negatives (those
    # that contain no faces), and neither (those that contain false positives
    # or false negatives).

    # after manually sorting the downloaded files, make the training set
    # by downloading the original images (w/o overlayed boxes) corresponding to
    # the manually chosen positives and negatives
    #make_training_set(path_hdfs, path_disp_pos, path_disp_neg,
    #                  path_pos, path_neg, pos_file, neg_file, max_count)

    # train classifier on a very small dataset
    train_classifier(pos_file, neg_file, path_out,
                     nneg=50, npos=100,
                     nstages=5, memory=500,
                     minhitrate=.9, maxfalsealarm=.5)


if __name__ == "__main__":
    main()
