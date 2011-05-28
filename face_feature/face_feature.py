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


import cv
import numpy as np


class Eigenfaces(object):

    def __init__(self, images=None, vectors=None, verbose=False):
        self.MODES = [('opencv', 'gray', 32)]
        self.verbose = verbose
        if not images == None and not vectors == None:
            self.train(images, vectors)

    def train(self, images, vectors):
        if images == None:
            raise ValueError('images must contain at least one image')
        if vectors == None:
            raise ValueError('vectors must contain at least one index')

        # assemble image matrix, subtract mean
        X = np.array([np.asarray(cv.GetMat(i)).ravel() for i in images])
        self.mean = np.mean(X, 0)
        for x in X:
            x = x - self.mean
        # assume that the number of images is smaller than the # of pixels
        M = np.dot(X, X.T)
        es, vs = np.linalg.eigvalsh(M)
        for v in vs:
            v = np.dot(X.T, v)         # get e.v. of X^T*X from that of X*X^T
            v = v / np.linalg.norm(v)  # normalize each eigenvector

        # order eigenvalues by
        ordering = sorted([(e, i) for (i, e) in enumerate(es)], reverse=True)
        indexes = np.array(ordering).take(vectors, 0)[:, 1]
        self.vectors = vectors.take(indexes, 1)

    def make_features(self, image_cv):
        image = np.asarray(cv.GetMat(image_cv), dtype=np.float32).ravel()
        out = np.dot(image - self.mean, self.vectors)
        return [out]
