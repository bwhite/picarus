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


class Mapper(object):
    def __init__(self):
        # [image_id] = list of clust_ids
        self._assignments = self._load_assignments()

    def _load_assignments(self):
        out = {}  # [image_id] = list of clust_ids
        with open(os.environ['ASSIGNMENTS_FN']) as fp:
            for clust_ind, image_id in pickle.load(fp):
                out.setdefault(image_id, []).append(clust_ind)
        return out

    def map(self, image_id, image_data):
        """Take in an image, if it is one we want then output it

        Args:
            name: unique image id
            image_data: Binary image data

        Yields:
            A tuple in the form of (key, value)
            key: cluster ind
            value: (image_id, image_data)
        """
        try:
            for cluster_ind in self._assignments[image_id]:
                yield cluster_ind, (image_id, image_data)
        except KeyError:
            pass

if __name__ == "__main__":
    if hadoopy.run(Mapper):
        hadoopy.print_doc_quit(__doc__)
