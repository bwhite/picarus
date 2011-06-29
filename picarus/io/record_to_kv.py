import hadoopy
import picarus


def mapper(key, value):
    """

    Args:
        key: image_hash
        value: record (see IO docs)

    Yields:
        A tuple in the form of (key, value)
        key: image_hash
        value: binary file data
    """
    fp = picarus.io._record_to_fp(value)
    yield key, fp.read()


if __name__ == '__main__':
    hadoopy.run(mapper)
