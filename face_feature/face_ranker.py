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
Hadoopy Face Ranker; ranks input face images by their distance in
feature space (Eigenfaces).
"""

__author__ = 'Vlad I. Morariu <morariu@umd.edu>'
__license__ = 'GPL V3'

import hadoopy
from PIL import Image
import imfeat
import cStringIO as StringIO
import cv
import numpy as np
import cPickle as pickle
import os
# not used directly here, but it needs to be packaged along
from picarus.vision import face_feature


class Mapper(object):

    def __init__(self):
        self._exemplar = pickle.load(open(os.environ['EXEMPLAR_FN'], 'rb'))
        self._feat = pickle.load(open(os.environ['FEATURE_FN'], 'rb'))
        self._size = (64, 64)  # hardcoded for now

    def _compute_face_distance(self, gray):
        # resize to the fixed size the feature was trained on
        # TODO(Vlad): do this in eigenfaces feature code
        fixed_size_gray = cv.CreateImage(self._size, 8, 3)
        cv.Resize(gray, fixed_size_gray, cv.CV_INTER_LINEAR)
        f = imfeat.compute(self._feat, fixed_size_gray)[0]
        # TODO(Vlad) replace w/ distpy
        return np.linalg.norm(self._exemplar - f)

    def _load_cv_image(self, value):
        return imfeat.convert_image(Image.open(StringIO.StringIO(value)),
                                    [('opencv', 'bgr', 8)])

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
        yield dist, (key, value)


def reducer(key, values):
    """Identity reducer"""
    for value in values:
        yield key, value


if __name__ == "__main__":
    hadoopy.run(Mapper, reducer, doc=__doc__)
