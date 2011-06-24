#!usr/bin/env python
import hadoopy
import StringIO
import Image
import os


def mapper(image_hash, image_data):
    thumb_size = int(os.environ['THUMB_SIZE'])
    image = Image.open(StringIO.StringIO(image_data))
    image.thumbnail((thumb_size, thumb_size))
    image = image.convert('RGB')
    s = StringIO.StringIO()
    image.save(s, 'JPEG')
    s.seek(0)

    yield image_hash, s.buf


if __name__ == '__main__':
    hadoopy.run(mapper)
