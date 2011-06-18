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

__author__ = 'Brandyn A. White <bwhite@cs.umd.edu>'
__license__ = 'GPL V3'

import hadoopy
import Image
import imfeat
import cStringIO as StringIO
import os
import cv


class Mapper(object):

    def __init__(self):
        path = 'haarcascade_frontalface_default.xml'
        if os.path.exists(path):
            self._cascade = cv.Load(path)
        else:
            path = 'fixtures/haarcascade_frontalface_default.xml'
            if os.path.exists(path):
                self._cascade = cv.Load(path)
            else:
                raise ValueError("Can't find .xml file!")
        self._output_boxes = 'OUTPUT_BOXES' in os.environ

    def _detect_faces(self, img):
        min_size = (20, 20)
        image_scale = 2
        haar_scale = 1.2
        min_neighbors = 2
        haar_flags = 0
        if img.nChannels == 3:
            gray = cv.CreateImage((img.width, img.height), 8, 1)
            cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        else:
            gray = img
        small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                                    cv.Round(img.height / image_scale)), 8, 1)
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
        cv.EqualizeHist(small_img, small_img)
        faces = cv.HaarDetectObjects(small_img, self._cascade,
                                     cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags,
                                     min_size)
        scaled_faces = [(x * image_scale, y * image_scale,
                          w * image_scale, h * image_scale)
                        for (x, y, w, h), n in faces]
        return [(x, y, x + w, y + h) for x, y, w, h in scaled_faces]

    def _load_cv_image(self, value):
        image = Image.open(StringIO.StringIO(value))
        image = image.convert('RGB')
        return image, imfeat.convert_image(image, [('opencv', 'rgb', 8)])

    def map(self, key, value):
        """
        Args:
            key: Image name
            value: Image as jpeg byte data

        Yields:
            A tuple in the form of (key, value)
            key: Imagename-face-x0<x_tl_val>-y0<y_tl_val>-x1<x_br_val>-y1<y_br_val>
            value: Cropped face binary data
        """
        try:
            image_pil, image_cv = self._load_cv_image(value)
        except:
            hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
            return
        faces = self._detect_faces(image_cv)
        if not faces:
            return
        if self._output_boxes:
            yield key, (value, faces)
        else:
            for x0, y0, x1, y1 in faces:
                image_pil_crop = image_pil.crop((x0, y0, x1, y1))
                out_fp = StringIO.StringIO()
                image_pil_crop.save(out_fp, 'JPEG')
                out_fp.seek(0)
                yield '%s-face-x0%d-y0%d-x1%d-y1%d' % (key, x0, y0, x1, y1), out_fp.read()

if __name__ == "__main__":
    hadoopy.run(Mapper, doc=__doc__)
