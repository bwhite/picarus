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
from PIL import Image
import imfeat
import cStringIO as StringIO
import cv
import os
import glob
import subprocess
import cPickle as pickle
import argparse


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


def save_display_images(path_hdfs, path_local, min_count,
                        max_count, key_to_path=None):
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
        if count >= min_count:
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
    # save the bounding boxes in a pickle file in each directory
    boxes = {pos_dir : {}, neg_dir : {}}
    # the following two files will contain the list of positive/negative
    # images for training the OpenCV face detector
    pos_fp = open(pos_file, 'w')
    neg_fp = open(neg_file, 'w')
    count = 0
    for k, (i, bs) in hadoopy.readtb(path_hdfs):
        try:
            path = key_to_path[k]
            # save the face bounding boxes for this image
            boxes[path][k] = bs
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
    # save the bounding boxes in a pickle file
    for (path, bs) in boxes.items():
        with open('%s/boxes.pkl' % path, 'wb') as f:
            pickle.dump(bs, f)


def train_classifier(pos_file, neg_file, out_dir,
                     nneg=3000, npos=7000,
                     nstages=20, nsplits=3,
                     memory=500,
                     minhitrate=.999, maxfalsealarm=.5,
                     size=(20, 20)):
    """
    Trains an object detector using OpenCV's haartraining code.  The default
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


def make_eigenfaces_training_set(inputdir, outputdir):
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    with open('%s/boxes.pkl' % inputdir, 'rb') as f:
        boxes = pickle.load(f)
    for k, bs in boxes.items():
        image = Image.open('%s/%s.jpg' % (inputdir, k))
        image = image.convert('RGB')
        for x0, y0, x1, y1 in bs:
            image_crop = image.crop((x0, y0, x1, y1))
            fn = '%s/%s-face-x0%d-y0%d-x1%d-y1%d.jpg' % (
                outputdir, k, x0, y0, x1, y1)
            image_crop.save(fn, 'JPEG')


def main():
    # defaults
    default_hdfs = '/user/root/flickr_hash_faces7'
    default_min = 0
    default_max = 4000
    default_dispneither = 'faces_disp_neither'
    default_disppos = 'faces_disp_pos'
    default_dispneg = 'faces_disp_neg'
    default_pos = 'faces_pos'
    default_neg = 'faces_neg'
    default_posfile = 'faces_train_pos.txt'
    default_negfile = 'faces_train_neg.txt'
    default_classifier = 'faces_classifier'
    default_cropdir = 'faces_cropped'
    
    parser = argparse.ArgumentParser(
        description='Face detector and feature training code. Can be used to '
        'download images with detected faces from HDFS, sort them manually '
        'into positive/negative samples, create an OpenCV classifier training '
        'dataset, train an OpenCV detector, and create a dataset of cropped '
        'faces to train face features.')
    # parameters for downloading flickr files with detected faces
    parser.add_argument('--hdfs', type=str,
                        help='HDFS path containing the output of the face-finder. '
                        '(default \'%s\')' % default_hdfs,
                        default=default_hdfs)
    parser.add_argument('--min', type=int, help='index of first image to consider '
                        'from sequence file (default %i)' % default_min,
                        default=default_min)
    parser.add_argument('--max', type=int, help='index of last image to consider '
                        'from sequence file (default %i)' % default_max,
                        default=default_max)
    # args for displaying and manually sorting/annotating images with detected faces (downloaded from above)
    parser.add_argument('--dispneither', type=str,
                        help='Directory to which display faces will be saved before annotation'
                        '(see --annotate and --checkpos) (default \'%s\')' % default_dispneither,
                        default=default_dispneither)
    parser.add_argument('--disppos', type=str,
                        help='Directory to which positive display faces will be moved during manual annotation '
                        '(see --annotate and --checkpos) (default \'%s\')' % default_disppos,
                        default=default_disppos)
    parser.add_argument('--dispneg', type=str,
                        help='Directory to which negative display faces will be moved during manual annotation '
                        '(see --annotate and --checkpos) (default \'%s\')' % default_dispneg,
                        default=default_dispneg)
    # directories in which training images will be downloaded
    parser.add_argument('--pos', type=str,
                        help='Directory to which positive training images will be saved '
                        '(default \'%s\')' % default_pos,
                        default=default_pos)
    parser.add_argument('--neg', type=str,
                        help='Directory to which negative training images will be saved '
                        '(default \'%s\')' % default_neg,
                        default=default_neg)
    # opencv classifier training files
    parser.add_argument('--posfile', type=str,
                        help='File listing the positive training images and boxes (from --pos directory) '
                        '(default \'%s\')' % default_posfile,
                        default=default_posfile)
    parser.add_argument('--negfile', type=str,
                        help='File listing the negative training images (from --neg directory) '
                        '(default \'%s\')' % default_negfile,
                        default=default_negfile)
    parser.add_argument('--classifier', type=str,
                        help='Trained classifier path '
                        '(default \'%s\')' % default_classifier,
                        default=default_classifier)
    parser.add_argument('--cropdir', type=str,
                        help='Place cropped faces here (from the positive dir --pos) '
                        '(default \'%s\')' % default_cropdir,
                        default=default_cropdir)
    # flags enabling various training steps (nothing happens, by default)
    parser.add_argument('--downloaddisp', action='store_true',
                        help='Download and save display images from HDFS.')
    parser.add_argument('--annotate', action='store_true',
                        help='Annotate positive/negative training images.')
    parser.add_argument('--checkpos', action='store_true',
                        help='Check (and modify, if needed) the positive training set.')
    parser.add_argument('--downloadtrain', action='store_true',
                        help='Download positive and negative images corresponding to '
                        '--disppos and --dispneg paths into --pos and --neg paths.')
    parser.add_argument('--train', action='store_true',
                        help='Train an opencv classifier.')
    parser.add_argument('--crop', action='store_true',
                        help='Crop faces from positive samples.')
    
    args = parser.parse_args()

    # the paths for storing images in which all faces were detected
    # and where some or no faces were detected
    key_to_path_pkl = 'faces_key_to_path.pkl'

    # load paths of images that have already been manually sorted
    key_to_path = get_existing_paths(
        args.disppos, args.dispneither, args.dispneg)
    # load already saved paths from pickle file
    if os.path.exists(key_to_path_pkl):
        with open(key_to_path_pkl, 'r') as f:
            key_to_path.update(pickle.load(f))
            
    # download images from hdfs and place them in the 'neither' directory,
    # unless they have already been moved to some other directory
    if args.downloaddisp:
        save_display_images(args.hdfs, args.dispneither,
                            args.min, args.max, key_to_path)

    # now manually sort the display images into ones that should be used as
    # positives (those in which all people are detected), negatives (those
    # that contain no faces), and neither (those that contain false positives
    # or false negatives).
    if args.annotate:
        
        cmd = ('python -m image_server --thumbsize 200 --imagedir %s '
               '--movedirs %s --movedirs %s '
               '--limit 500 --port 20001' % (
                   args.dispneither, args.disppos, args.dispneg))
        try:
            subprocess.call(cmd.split())
        except KeyboardInterrupt:  # the only way to quit the image_server is via Ctrl+C
            pass
    # double-check positives
    if args.checkpos:
        cmd = ('python -m image_server --thumbsize 200 --imagedir %s '
               '--movedirs %s --movedirs %s '
               '--limit 500 --port 20001' % (
                   args.disppos, args.dispneither, args.dispneg))
        try:
            subprocess.call(cmd.split())
        except KeyboardInterrupt:  # the only way to quit the image_server is via Ctrl+C
            pass
 
    # after manually sorting the downloaded files, make the training set
    # by downloading the original images (w/o overlayed boxes) corresponding to
    # the manually chosen positives and negatives
    if args.downloadtrain:
        make_training_set(args.hdfs, args.disppos, args.dispneg,
                          args.pos, args.neg, args.posfile, args.negfile, args.max)

    # train classifier on a very small dataset (use the defaults of train_classifier9)
    # to train a real clasifier--this might take a few days)
    if args.train:
        train_classifier(args.posfile, args.negfile, args.classifier,
                         nneg=50, npos=100,
                         nstages=5, memory=500,
                         minhitrate=.9, maxfalsealarm=.5)

    # create a training set for the eigenface feature using the positive images chosen above
    if args.crop:
        make_eigenfaces_training_set(args.pos, args.cropdir)
    
    # reload existing paths and save to a pickle file
    key_to_path.update(get_existing_paths(
        args.disppos, args.dispneither, args.dispneg))
    with open(key_to_path_pkl, 'w') as f:
        pickle.dump(key_to_path, f)


if __name__ == "__main__":
    main()
