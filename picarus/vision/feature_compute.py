#!/usr/bin/env python
import hadoopy
import imfeat
import os
import sys
import numpy as np
import json
import base64
import picarus._features as features
from picarus._importer import call_import


class Mapper(object):

    def __init__(self):
        try:
            self._feat = features.select_feature(os.environ['FEATURE'])
        except KeyError:
            self._feat = call_import(json.loads(base64.b64decode(os.environ['FEATURE'])))

    def map(self, name, image_or_data):
        if isinstance(image_or_data, str):
            try:
                image = imfeat.image_fromstring(image_or_data)
            except:
                hadoopy.counter('DATA_ERRORS', 'ImageLoadError')
                return
        else:
            image = image_or_data
        yield name, self._feat(image)


if __name__ == '__main__':
    hadoopy.run(Mapper)
