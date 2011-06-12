import hadoopy


def mapper(k, v):
    yield 0, 0

hadoopy.run(mapper)
