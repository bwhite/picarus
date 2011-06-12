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

__author__ =  'Vlad I. Morariu <morariu@umd.edu>'
__license__ = 'GPL V3'

import hadoopy
import os
import imfeat
import Image
import cStringIO as StringIO
import glob
import Image
import shutil


def test_tb(path):
    # test that we can read each file using _load_cv_image
    for (key, val) in hadoopy.readtb(path):
        print(key)
        i = imfeat.convert_image(Image.open(StringIO.StringIO(val)),
                                [('opencv', 'gray', 8)])


def write_tb(path, fold=None):
    fddb_path = '/home/morariu/downloads/fddb'
    if fold == None:
        folds_glob = fddb_path + '/FDDB-folds/FDDB-fold-??.txt'
    else:
        folds_glob = fddb_path + '/FDDB-folds/FDDB-fold-%02i.txt' % fold

    if hadoopy.exists(path):
        # do nothing if the file already exists
        pass
    else:
        # otherwise, find all images in the fddb folds and put them  on hdfs
        names = []
        for fn in glob.glob(folds_glob):
            with open(fn, 'r') as fp:
                names.extend(['%s/%s.jpg' % (fddb_path, l) 
                              for l in fp.read().strip().split('\n')])
        # print message about filenames that do not exist
        for n in names:
            if not os.path.exists(n):
                print('"%s" does not exist!' % n)
        # remove those filenames from the list
        names = filter(os.path.exists, names)
        # write the images to tb files
        hadoopy.writetb(path, [(n, open(n, 'rb').read()) for n in names])


def copy_local(path, fold=None):
    fddb_path = '/home/morariu/downloads/fddb'
    if fold == None:
        folds_glob = fddb_path + '/FDDB-folds/FDDB-fold-??.txt'
    else:
        folds_glob = fddb_path + '/FDDB-folds/FDDB-fold-01.txt'

    if os.path.exists(path):
        # do nothing if the file already exists
        pass
    else:
        names = []
        for fn in glob.glob(folds_glob):
            with open(fn, 'r') as fp:
                names.extend(['%s/%s.jpg' % (fddb_path, l)
                              for l in fp.read().strip().split('\n')])
        # print message about filenames that do not exist
        for n in names:
            if not os.path.exists(n):
                print('"%s" does not exist!' % n)
        # remove those filenames from the list
        names = filter(os.path.exists, names)
        # write the images to tb files
        if not os.path.exists(path):
            os.makedirs(path)
        for n in names:
            shutil.copy2(n, '%s/%s' % (
                    path, n.replace(fddb_path + '/', '').replace('/', '_')))

            
if __name__ == '__main__':    
    #write_tb('fddb_test_data/fold_01.tb', 1)
    #test_tb('fddb_test_data/fold_01.tb')
    #write_tb('fddb_test_data/all_folds.tb', 1)
    #test_tb('fddb_test_data/all_folds.tb')
    copy_local('/home/tp/data/fddb_test_data/fold_01', 1)
    copy_local('/home/tp/data/fddb_test_data/all_folds')
