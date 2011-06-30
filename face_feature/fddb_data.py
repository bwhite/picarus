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
import shutil
import urllib2
import tarfile


def download_data(data_path='data'):
    """
    If {data_path}/fddb does not exist, this function creates the folder
    and downloads extracts the fddb database into it.
    """
    fddb_path = '%s/fddb' % data_path
    dl_urls = ['http://tamaraberg.com/faceDataset/originalPics.tar.gz',
               'http://vis-www.cs.umass.edu/fddb/FDDB-folds.tgz']
    if not os.path.isdir(fddb_path):
        os.makedirs(fddb_path)
        for dl_url in dl_urls:
            print('Downloading \'%s\' to \'%s\'...' % (dl_url, fddb_path))
            u = urllib2.urlopen(dl_url)
            tar_name = '%s/%s' % (fddb_path, os.path.basename(dl_url))
            with open(tar_name, 'wb') as fp:
                data = u.read(4096)
                while data:
                    fp.write(data)
                    data = u.read(4096)
            tar_file = tarfile.open(tar_name, 'r', errorlevel=0)
            tar_file.extractall(fddb_path)
                                                                

def test_tb(path):
    """
    This function tests the sequence file at 'path' (on hdfs) by
    reading the images from it.
    """
    # test that we can read each file using _load_cv_image
    for (key, val) in hadoopy.readtb(path):
        print(key)
        i = imfeat.convert_image(Image.open(StringIO.StringIO(val)),
                                [('opencv', 'gray', 8)])


def write_tb(path, fold=None, data_path='data'):
    """
    Copy all images in the specified fddb folds and put them on hdfs.
    If folds=None (default), then all images from all folds are copied.
    If the fddb dataset does not already exist in {data_path}/fddb,
    then that directory is created and the fddb is downloaded there.
    """
    fddb_path = '%s/fddb' % data_path
    # download fddb, if necessary
    if not os.path.isdir(fddb_path):
        download_data(data_path)
    if fold == None:
        folds_glob = fddb_path + '/FDDB-folds/FDDB-fold-??.txt'
    else:
        folds_glob = fddb_path + '/FDDB-folds/FDDB-fold-%02i.txt' % fold
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


def copy_local(path, fold=None, data_path='data'):
    """
    Copy all images in the specified fddb folds to a local folder.
    If folds=None (default), then all images from all folds are copied.
    If the fddb dataset does not already exist in {data_path}/fddb,
    then that directory is created and the fddb is downloaded there.
    """
    fddb_path = '%/fddb' % data_path
    if not os.path.isdir(fddb_path):
        download_data(data_path)
    if fold == None:
        folds_glob = fddb_path + '/FDDB-folds/FDDB-fold-??.txt'
    else:
        folds_glob = fddb_path + '/FDDB-folds/FDDB-fold-01.txt'
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
    write_tb('fddb_test_data/all_folds.tb')
    #test_tb('fddb_test_data/all_folds.tb')
    #copy_local('/home/tp/data/fddb_test_data/fold_01', 1)
    #copy_local('/home/tp/data/fddb_test_data/all_folds')
