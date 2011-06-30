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
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class Test(unittest.TestCase):

    def test_0(self):
        # test if the code runs without errors
        images = [cv.LoadImage(x)
                  for x in lfwcrop_data.get_unique_lfw_training_images('data')[:100]]
        vectors = range(3, 64)
        feat = face_feature.Eigenfaces(images, vectors)
        out = imfeat.compute(feat, images[0])

        self.assertEqual(len(feat.mean), feat.vectors.shape[0])
        self.assertEqual(1, len(out))
        self.assertEqual(61, feat.vectors.shape[1])
        self.assertEqual(61, len(out[0]))


if __name__ == '__main__':
    unittest.main()
