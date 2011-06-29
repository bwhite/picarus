import hadoopy
import hashlib
import os


def mapper(key, value):
    """

    Args:
        key: image_hash
        value: binary file data

    Yields:
        A tuple in the form of (key, value)
        key: image_hash
        value: record (see IO docs)
    """
    sha1 = hashlib.sha1(value).hexdigest()
    full_path = '%s/%s.%s' % (os.environ['BASE_PATH'], key, os.environ['EXTENSION'])
    yield key, {'sha1': sha1, 'full_path': full_path, 'data': value,
                'extension': os.environ['EXTENSION']}


if __name__ == '__main__':
    hadoopy.run(mapper)
