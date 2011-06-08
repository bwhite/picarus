import hadoopy
import tempfile
import cStringIO as StringIO
import Image


class Mapper(object):

    def __init__(self):
        pass

    def map(hash, video_data):
        """

        Args:
            hash: Video data md5 hash
            video_data: Raw binary data

        Yields:
            A tuple in the form of (hash, image_data)
            hash: 
            image_data: Raw binary data
        """
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(video_data)
            fp.flush()
            #
        out = StringIO.StringIO()
        Image.save(out, 'jpg')
        out.seek(0)
        yield hash, out.read()

if __name__ == '__main__':
    hadoopy.run(Mapper)
