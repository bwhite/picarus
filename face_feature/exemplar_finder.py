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

"""Hadoopy Eigenfaces feature test"""

__author__ = 'Vlad I. Morariu <morariu@umd.edu>'
__license__ = 'GPL V3'

import hadoopy
import Image
import imfeat
import cStringIO as StringIO
import cv
import numpy as np
import cPickle


def get_face_feature():
    """
    Get the feature of an image from the lfw dataset.  This will be
    hard-coded below for testing purposes.
    """
    # Bush has most images in lfw training set
    fn = '/home/morariu/downloads/lfwcrop_color/faces/George_W_Bush_0026.ppm'
    im = cv.LoadImage(fn)
    pkl_fn = 'eigenfaces_lfw_cropped.pkl'
    with open(pkl_fn, 'r') as fp:
        feat = cPickle.load(fp)
    return imfeat.compute(feat, im)[0]


def get_face_feature_hardcoded():
    return np.array(
        [0.2762576, 0.27256906, 1.70179176, 0.17377375, 1.87855041,
         1.32401788, -0.57568979, -0.176221, 0.96265972, -0.33039954,
         1.51071942, 0.37406468, 1.2077049, 0.4285641, -0.66499186,
         0.67021221, 0.41837472, -1.48721039, 0.42631847, -0.45617098,
         -0.2363046, 0.29525691, -0.07042997, 0.44689092, 0.73656243,
         0.56115109, -0.03644806, 0.11875051, 0.24915269, 0.59913337,
         -0.2993238, 0.26629299, -0.81638837, 0.01461185, -0.6385473 ,
         -0.0433887, 0.31900325, 0.08162703, -0.05487341, -0.08162712,
         0.15491676, -0.39614683, 0.50749218, 0.07716984, -0.23573144,
         0.52771103, 0.34838215, -0.6905238, -0.6828168, -0.11485191,
         -0.1389063 , 0.07891759, -0.03906267, 0.44505718, 0.09177706,
         -0.33152461, 0.20268679, 0.22922522, -0.10565381, 0.43324503,
         -0.21734388, -0.04742456], dtype='float64')


class Mapper(object):

    def __init__(self):
        self._exemplar = get_face_feature_hardcoded()
        pkl_fn = 'eigenfaces_lfw_cropped.pkl'
        with open(pkl_fn, 'r') as fp:
            self._feat = cPickle.load(fp)
        self._size = (64, 64)  # hardcoded for now

    def _compute_face_distance(self, gray):
        # resize to the fixed size the feature was trained on
        # TODO(Vlad): do this in eigenfaces feature code
        fixed_size_gray = cv.CreateImage(self._size, 8, 1)
        cv.Resize(gray, fixed_size_gray, cv.CV_INTER_LINEAR)
        f = imfeat.compute(self._feat, fixed_size_gray)[0]
        # TODO(Vlad) replace w/ distpy
        return np.linalg.norm(self._exemplar - f)

    def _load_cv_image(self, value):
        return imfeat.convert_image(Image.open(StringIO.StringIO(value)),
                                    [('opencv', 'gray', 8)])

    def map(self, key, value):
        """
        Args:
            key: Image name
            value: Image as jpeg byte data

        Yields:
            A tuple in the form of (key, value)
            key: Image name
            value: (image, faces) where image is the input value and faces is
                a list of ((x, y, w, h), n)
        """
        try:
            image = self._load_cv_image(value)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
            return
        dist = self._compute_face_distance(image)
        yield dist, value


def reducer(key, values):
    """Identity reducer"""
    for value in values:
        yield key, value


if __name__ == "__main__":
    hadoopy.run(Mapper, doc=__doc__)
