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

"""Hadoop K-means
"""

__author__ = 'Brandyn A. White <bwhite@cs.umd.edu>'
__license__ = 'GPL V3'

import cPickle as pickle
import numpy as np
import hadoopy
import distpy
import os
import random
import functools
from kmeans import Mapper, Reducer


def cluster(points, num_clusters, max_iters=50, norm='l2sqr'):
    clusters = random.sample(points, num_clusters)
    for cur_iter in range(max_iters):
        mapper = functools.partial(Mapper, clusters=clusters)
        map_out = hadoopy.Test.call_map(mapper, test_in)
        reduce_in = hadoopy.Test.shuffle_kv(map_out)
        clusters = [x[1] for x in self.call_reduce(Reducer, reduce_in)]
