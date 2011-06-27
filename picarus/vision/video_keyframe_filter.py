#!/usr/bin/env python
import hadoopy
import numpy as np


def mapper(key, image_metadata):
    (tag, hash) = key
    if tag == 'frame':
        yield hash, image_metadata


if __name__ == '__main__':
    hadoopy.run(mapper)
