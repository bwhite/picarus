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
import hadoopy
import os
import numpy as np
import distpy
import picarus


class Mapper(object):

    def __init__(self):
        self._norm = distpy.L2Sqr()
        self._clusters = self._load_clusters()

    def _load_clusters(self):
        with open(os.environ['CLUSTERS_FN']) as fp:
            return np.ascontiguousarray(pickle.load(fp), dtype=np.float64)

    @picarus.valid_image_check
    def map(self, image_id, point_or_image):
        """Take in a point, find its NN or if an image, pass through.

        Args:
            image_id: image id
            point_or_image: numpy array or binary image data

        Yields:
            A tuple in the form of (key, value)
            key: image_id
            value: nearest cluster index (int) or image_data (str)
        """
        if isinstance(point_or_image, str):
            yield image_id, point_or_image
        else:
            n = self._norm.nn(self._clusters, point_or_image)[1]
            yield image_id, n


class Reducer(object):

    def __init__(self):
        pass

    def reduce(self, key, values):
        """Take in a series of points, find their sum.

        Args:
            key: (see mapper)
            values: (see mapper)

        Yields:
            A tuple in the form of (key, value)
            key: cluster index (int)
            value: (image_id, image_data)
        """
        image_data = None
        cluster_ind = None
        for value in values:
            if isinstance(value, str):
                image_data = value
            else:
                cluster_ind = value
        if image_data is None or cluster_ind is None:
            hadoopy.counter('DATA_ERROR', 'MISSING_DATA_OR_FEAT')
        else:
            yield cluster_ind, (key, image_data)


if __name__ == "__main__":
    if hadoopy.run(Mapper, Reducer):
        hadoopy.print_doc_quit(__doc__)
