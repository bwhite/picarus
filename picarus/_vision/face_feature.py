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
import imfeat


class Eigenfaces(object):

    def __init__(self, images=None, vectors=None, verbose=False):
        self.MODES = [('opencv', 'gray', 32)]
        self.verbose = verbose
        if not images == None:
            images = [imfeat.convert_image(i, self.MODES) for i in images]
            self.train(images, vectors)

    def train(self, images, vectors):
        if images == None or len(images) == 0:
            raise ValueError('\'images\' must contain at least one image')
        if vectors == None or len(vectors) == 0:
            # discard the first 3 eigenvectors
            vectors = range(3, min(len(images), 65))

        # assemble image matrix, subtract mean
        X = np.array([np.asarray(cv.GetMat(i)).ravel() for i in images])
        self.mean = np.mean(X, 0)
        X = X - self.mean

        # assume that the number of images is smaller than the # of pixels
        M = np.dot(X, X.T)
        es, vs = np.linalg.eigh(M)
        vs = np.dot(X.T, vs)        # get e.v. of X^T*X from that of X*X^T
        for i in range(vs.shape[1]):
            vs[:, i] /= np.linalg.norm(vs[:, i])  # normalize each eigenvector

        # order eigenvalues by magnitude and keep only desired vectors
        ordering = sorted([(e, i) for (i, e) in enumerate(es)], reverse=True)
        indexes = np.array(ordering).take(vectors, 0)[:, 1]
        self.vectors = vs.take(indexes.tolist(), 1)

    def make_features(self, image_cv):
        image = np.asarray(cv.GetMat(image_cv), dtype=np.float32).ravel()
        out = np.dot(image - self.mean, self.vectors)
        return [out]


def main():
    import glob
    images = [cv.LoadImage(x)
              for x in glob.glob('/home/morariu/downloads/lfwcrop_color/faces/*')[:100]]
    vectors = range(4, 10)
    feat = Eigenfaces(images, vectors)
    out = imfeat.compute(feat, images[0])
    print(out)


if __name__ == "__main__":
    main()
