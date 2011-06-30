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
    try:
        fp = picarus.io._record_to_fp(value)
    except IOError:
        hadoopy.counter('INPUT_ERROR', 'REMOTE_READ_FAILED')
        return
    yield key, fp.read()


if __name__ == '__main__':
    hadoopy.run(mapper)
