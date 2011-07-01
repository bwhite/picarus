#!usr/bin/env python
import hadoopy
import StringIO
import Image
import os
import numpy as np
import picarus


def mapper(key, value):
    """
    Args:
        key, value:
           either of - the output of clustering (/partition or /samples),
                     - the output of video keyframing (/allframes)
                     - (hash,image_data) input
                     - (hash,image_metadata) input
    Env vars:
        IMAGE_TYPE: record, cluster, kv, frame
        THUMB_SIZE: longest dimension for the thumbnail images

    Yields:
        image_hash, image_data: serialized jpeg data for thumbnail
    """
    if os.environ['IMAGE_TYPE'] == 'record':
        # Image input format
        image_hash, image_metadata = key, value
        image_file = picarus.io._record_to_file(image_metadata)

    elif os.environ['IMAGE_TYPE'] == 'cluster':
        # Cluster output /partition or /sample
        cluster_index, (image_hash, image_data) = key, value
        image_file = StringIO.StringIO(image_data)

    elif os.environ['IMAGE_TYPE'] == 'kv':
        # hash, image bytes
        image_hash, image_data = key, value
        image_file = StringIO.StringIO(image_data)

    elif os.environ['IMAGE_TYPE'] == 'frame':
        image_hash, image_metadata = key, value
        image_file = StringIO.StringIO(image_metadata['image_data'])

    thumb_size = int(os.environ['THUMB_SIZE'])
    try:
        image = Image.open(image_file)
        image.thumbnail((thumb_size, thumb_size))
    except:
        hadoopy.counter('INPUT_ERROR', 'IMAGE_DATA_ERROR')
    image = image.convert('RGB')
    s = StringIO.StringIO()
    image.save(s, 'JPEG')
    s.seek(0)

    # Output type: kv
    yield image_hash, s.buf


if __name__ == '__main__':
    hadoopy.run(mapper)
