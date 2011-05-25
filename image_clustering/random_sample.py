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

"""Random sampling of key/value pairs
"""

__author__ = 'Brandyn A. White <bwhite@cs.umd.edu>'
__license__ = 'GPL V3'

import hadoopy
import os
import bisect
import random


class Mapper(object):

    def __init__(self):
        self._sorted_rands = [float('inf')]  # (random)
        self._key_vals = {}  # [random] = (key, point)
        self._sample_size = os.environ['SAMPLE_SIZE']

    def map(self, key, value):
        """Take in points and output a random sample

        Args:
            key: Opaque (can be anything)
            value: Opaque (can be anything)
        """
        cur_rand = random.random()
        if cur_rand < self._sorted_rands[-1]:
            bisect.insort(self._sorted_rands, cur_rand)
            self._key_vals[cur_rand] = (key, value)
        if len(self._sorted_rands) > self._sample_size:
            del self._key_vals[self._sorted_rands[-1]]
            self._sorted_rands = self._sorted_rands[:-1]

    def close(self):
        """
        Yields:
            A tuple in the form of (key, value)
            key: Random float
            value: (Input key, Input value)
        """
        for rand in self._sorted_rands:
            try:
                yield rand, self._key_vals[rand]
            except KeyError:  # Ignore inf
                pass


class Reducer(object):

    def __init__(self):
        self._sample_size = os.environ['SAMPLE_SIZE']
        self._num_output = 0

    def reduce(self, rand, key_vals):
        """Take in a series of points, find their sum.

        Args:
            rand: Random float
            key_vals: Iterator of (Input key, Input value)

        Yields:
            A tuple in the form of (key, value)
            key: Input key
            value: Input value
        """
        for kv in key_vals:
            if self._sample_size <= self._num_output:
                break
            yield kv
            self._num_output += 1

if __name__ == "__main__":
    if hadoopy.run(Mapper, Reducer):
        hadoopy.print_doc_quit(__doc__)
