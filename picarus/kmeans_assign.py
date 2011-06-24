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


class Mapper(object):
    def __init__(self):
        self._norm = distpy.L2Sqr()
        self._clusters = self._load_clusters()

    def _load_clusters(self):
        with open(os.environ['CLUSTERS_FN']) as fp:
            return np.ascontiguousarray(pickle.load(fp), dtype=np.float64)

    def map(self, point_id, point):
        """Take in a point, find its NN.

        Args:
            point_id: point id
            point: numpy array

        Yields:
            A tuple in the form of (key, value)
            key: nearest cluster index (int)
            value: point_id
        """
        n = self._norm.nn(self._clusters, point)[1]
        yield '%d\t%f' % (n, random.random()), point_id


class Reducer(object):
    def __init__(self):
        self._num_samples = int(os.environ['NUM_SAMPLES'])
        self._cur_samples = 0
        self._cur_clust = None
    
    def reduce(self, composite, point_ids):
        """Take in a series of assignments, select a sample of them

        This uses a modified partitioner that only uses the first part of the
        key so that a uniform sampling is performed.

        Args:
            composite: clust_num\trandom
            point_id: point_id

        Yields:
            A tuple in the form of (key, value)
            key: cluster index (int)
            value: List of point_id's
        """
        n = int(composite.split('\t')[0])
        if n != self._cur_clust:
            self._cur_clust = n
            self._cur_samples = 0
        for point_id in point_ids:
            if self._num_samples <= self._cur_samples:
                break
            self._cur_samples += 1
            yield n, point_id


if __name__ == "__main__":
    if hadoopy.run(Mapper, Reducer):
        hadoopy.print_doc_quit(__doc__)
