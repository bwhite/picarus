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


class Mapper(object):
    def __init__(self):
        self._norm = distpy.L2Sqr()
        self._clusters = self._load_clusters()
        self._cluster_sums = {}

    def _load_clusters(self):
        with open(os.environ['CLUSTERS_FN']) as fp:
            return np.ascontiguousarray(pickle.load(fp), dtype=np.float64)

    def _extend_point(self, point):
        point = np.resize(point, len(point) + 1)
        point[-1] = 1
        return point

    def map(self, unused_i, point):
        """Take in a point, find its NN.

        Args:
            unused_i: point id (unused)
            point: numpy array

        Yields:
            A tuple in the form of (key, value)
            key: nearest cluster index (int)
            value: partial sum (numpy array)
        """
        n = self._norm.nn(self._clusters, point)[1]
        point = self._extend_point(point)
        self._cluster_sums[n] = self._cluster_sums.get(n, 0) + point

    def close(self):
        for n, point in self._cluster_sums.items():
            yield n, point


class Reducer(object):
    def _compute_centroid(self, s):
        return s[0:-1] / s[-1]

    def reduce(self, n, points):
        """Take in a series of points, find their sum.

        Args:
            n: nearest cluster index (int)
            points: partial sums (numpy arrays)

        Yields:
            A tuple in the form of (key, value)
            key: cluster index (int)
            value: cluster center (numpy array)
        """
        s = 0
        for p in points:
            s += p
        m = self._compute_centroid(s)
        yield n, m


if __name__ == "__main__":
    if hadoopy.run(Mapper, Reducer):
        hadoopy.print_doc_quit(__doc__)
