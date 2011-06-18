#!/usr/bin/env python
import hadoopy
import vidfeat
import tempfile
import StringIO


def grab_frame(file_name):
    frame_iter = vidfeat.convert_video_ffmpeg(file_name,
                                              ('frameiter', ['RGB']),
                                              True)
    return frame_iter.next()[2]


def mapper(hash, video_data):
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
    hadoopy.run(mapper)
