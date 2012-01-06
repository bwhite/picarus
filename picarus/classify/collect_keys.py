#!/usr/bin/env python
import hadoopy
import numpy as np


def mapper(k, v):
    yield 'keys', k


def reducer(k, vs):
    yield k, list(vs)

if __name__ == '__main__':
    hadoopy.run(mapper, reducer)
