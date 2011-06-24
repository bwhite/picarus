#!/usr/bin/env python
import hadoopy
import numpy as np


def mapper(key, image_data):
    (tag, hash) = key
    print key
    if tag == 'frame':
        yield hash, image_data


if __name__ == '__main__':
    hadoopy.run(mapper)
