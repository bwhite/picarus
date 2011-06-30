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
"""
Get lfwcrop data (download dataset if necessary).
"""
__author__ = 'Vlad I. Morariu <morariu@umd.edu>'
__license__ = 'GPL V3'


import zipfile
import urllib2
import os


def download_data(data_path='data'):
    dl_url = 'http://itee.uq.edu.au/~conrad/lfwcrop/lfwcrop_color.zip'
    u = urllib2.urlopen(dl_url)
    zip_name = '%s/lfwcrop_color.zip' % data_path
    print('Downloading \'%s\' to \'%s\'...' % (dl_url, zip_name))
    with open(zip_name, 'wb') as fp:
        data = u.read(4096)
        while data:
            fp.write(data)
            data = u.read(4096)
    zip_file = zipfile.ZipFile(zip_name, 'r')
    zip_file.extractall(data_path)
        

def get_lfw_cropped_data(split='dv_train', data_path='data'):
    """
    Args:
    split: Dataset split, one of:
       'dv_train', 'dv_test',
       '01_train', '01_test',
       '02_train', '02_test',
       '03_train', '03_test',
       '04_train', '04_test',
       '05_train', '05_test',
       '06_train', '06_test',
       '07_train', '07_test',
       '08_train', '08_test',
       '09_train', '09_test',
       '10_train', '10_test'
       (default: 'dv_train')

    Returns:
    Dataset as specified by 'split'

    Data is in the form of out[[image_path1,image_path2]] = objects, where
    objects is {'class': class_name}.  Here classname is either
    'same' or 'diff' based on whether the images are of the same
    person or not.
    """
    lfwcrop_path = '%s/lfwcrop_color' % data_path
    if not os.path.isdir(lfwcrop_path):
        os.makedirs(lfwcrop_path)
        download_data(data_path)
    lists_path = '%s/lists' % lfwcrop_path
    faces_path = '%s/faces' % lfwcrop_path
    splitnums = set(map(lambda x: '%02i' % x, range(1, 11)) + ['dv'])
    splittypes = set(['train', 'test'])
    classnames = set(['same', 'diff'])

    components = split.lower().split('_')
    if(len(components) < 2  or len(components) > 3 or
       not components[0] in splitnums or
       not components[1] in splittypes or
       len(components) == 3 and not components[2] in classnames):
        raise ValueError('Unrecognized \'split\' value \'%s\'' % split)

    if(len(components) == 2):
        lists = [components + ['same'], components + ['diff']]
    else:
        lists = [components]

    out = {}
    for l in lists:
        with open('%s/%s.txt' % (lists_path, '_'.join(l)), 'r') as f:
            for line in f.read().strip().split('\n'):
                files = map(lambda x: '%s/%s.ppm' % (faces_path, x),
                            line.strip(' ').split())
                out[tuple(files)] = {'class' : l[-1]}
    return out


def get_unique_lfw_training_images(path='data'):
    train_data = get_lfw_cropped_data('01_train', path)
    test_data = get_lfw_cropped_data('01_test', path)
    # combine train and test folds to use all folds for training
    train_data.update(test_data)
    # get a list of unique training images
    train_fns = []
    for fnpair in train_data.keys():
        train_fns.extend(fnpair)
    train_fns = sorted(set(train_fns))
    return train_fns


if __name__ == '__main__':
    fn = get_unique_lfw_training_images('data')
    print('first ten filenames:')
    print(fn[0:10])
