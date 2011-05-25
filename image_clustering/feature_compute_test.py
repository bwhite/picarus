#!/usr/bin/env python
# (C) Copyright 2010 Brandyn A. White
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

"""Test Feature Computation
"""

__author__ = 'Brandyn A. White <bwhite@cs.umd.edu>'
__license__ = 'GPL V3'

import unittest
import hadoopy
import os
import pickle
import numpy as np
from feature_compute import mapper


lena_feat = [9.663899739583333e-05, 0.06362279256184895, 0.03119659423828125,
             0.04167811075846354, 0.06435139973958333, 0.07552846272786458,
             0.041782379150390625, 0.015076955159505209, 0.033376057942708336,
             0.09513092041015625, 0.09322230021158855, 0.06615447998046875,
             0.025521596272786457, 0.018885294596354168, 0.0010388692220052083,
             3.814697265625e-06, 0.030595143636067707, 0.14550272623697916,
             0.09968185424804688, 0.02907562255859375, 0.02182769775390625,
             0.006253560384114583, 0.0003954569498697917, 1.2715657552083333e-06]


class Test(hadoopy.Test):
    def __init__(self, *args, **kw):
        super(Test, self).__init__(*args, **kw)
        self.Mapper = mapper

    def test_map(self):
        test_in = [(0, open('lena.jpg').read())]
        test_out = [(0, np.array(lena_feat))]

        def tolist(s):
            return [(x[0], x[1].tolist()) for x in s]
        self.assertEqual(tolist(self.call_map(self.Mapper, test_in)),
                         tolist(test_out))

if __name__ == '__main__':
    unittest.main()
