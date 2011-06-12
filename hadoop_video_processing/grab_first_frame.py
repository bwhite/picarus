#!/usr/bin/env python
import hadoopy
import tempfile
import cStringIO as StringIO
import Image
import pyffmpeg
import PIL


def grab_frame(fn):
    stream = pyffmpeg.VideoStream()
    print('FN[%s]' % fn)
    stream.open(fn)
    out = stream.GetFrameNo(10)
    return out
            

class Mapper(object):

    def __init__(self):
        pass

    def map(self, hash, video_data):
        """

        Args:
            hash: Video data md5 hash
            video_data: Raw binary data

        Yields:
            A tuple in the form of (hash, image_data)
            hash: 
            image_data: Raw binary data
        """
        print(hash)
        with tempfile.NamedTemporaryFile(suffix='.avi') as fp:
            fp.write(video_data)
            fp.flush()
            image = grab_frame(fp.name)
        out = StringIO.StringIO()
        image.save(out, 'jpeg')
        out.seek(0)
        yield hash, out.read()

if __name__ == '__main__':
    hadoopy.run(Mapper)
