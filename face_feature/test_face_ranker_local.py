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

"""Simple functions to debug map/reduce job in isolation (no hdfs)."""

import cPickle


def debug_map_reduce(mapper, reducer, kv_map_in):
    # pass input (k, v) pairs through mapper
    kv_map_out = []
    for k, v in kv_map_in:
        kv_map_out.extend(mapper(k, v))

    # group values by key and sort before passing to reducer
    kv_red_in = {}
    for k, v in kv_map_in:
        kv_red_in.setdefault(k, []).append(v)
    kv_red_in = sorted(kv_red_in)

    # pass (k, vs) pairs through reducer
    kv_red_out = []
    for k, v in kv_map_in:
        kv_red_out.extend(reducer(k, [v]))

    # debug
    from IPython.Shell import IPShellEmbed
    IPShellEmbed()()


def debug_face_ranker():
    import face_ranker
    with open('out_face_finder.pkl', 'r') as f: kv_map_in = cPickle.load(f)
    mapper = face_ranker.Mapper()
    mapper_fn = mapper.map
    reducer_fn = face_ranker.reducer
    debug_map_reduce(mapper_fn, reducer_fn, kv_map_in)


def main():
    debug_face_ranker()


if __name__ == '__main__':
    main()
