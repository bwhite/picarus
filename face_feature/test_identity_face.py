#!/u85;95;0csr/bin/env python
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


import face_feature
import imfeat
import cv
import Image
import glob
import random
import numpy as np
try:
    import unittest2 as unittest
except ImportError:
    import unittest


def pil_to_cv(fp):
    return imfeat.convert_image(Image.open(fp), [('opencv', 'bgr', 8)])


def cv_to_array(image_cv):
    return np.asarray(cv.GetMat(image_cv), dtype=np.float32).ravel()


def resize(im, size):
    new_im = cv.CreateImage(size, im.depth, im.channels)
    cv.Resize(im, new_im)
    return new_im


class Test(unittest.TestCase):

    def test_identity(self):
        # for now, test if the code runs without errors
        images = [cv.LoadImage(x)
                  for x in random.sample(glob.glob(
                      '/home/morariu/downloads/lfwcrop_color/faces/*'), 100)]
        test_image = 'test_identity.jpg'
        im1 = cv.LoadImage(test_image)
        im2 = pil_to_cv(open(test_image))
        feat = face_feature.Eigenfaces(images)
        out1 = imfeat.compute(feat, resize(im1, cv.GetSize(images[0])))[0]
        out2 = imfeat.compute(feat, resize(im2, cv.GetSize(images[0])))[0]
        print('||feat(cv) - feat(pil)|| = %g' % (
            np.linalg.norm(out1 - out2)/len(out1)))
        print('||cv - pil|| = %g' % (np.linalg.norm(
            cv_to_array(im1)-cv_to_array(im2))/len(cv_to_array(im1))))


if __name__ == '__main__':
    unittest.main()
