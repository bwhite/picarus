#!/usr/bin/env python
import pyffmpeg
import StringIO
import hashlib
import json
import Image
import keyframe
import tempfile
import sys
import hadoopy


def keyframes(video, videohash, kf):
    boundaries = [0.0]
    for (frame_num, frame_time, frame), iskeyframe in kf(video):
        if iskeyframe:
            boundaries.append(frame_time)
    if boundaries[-1] < frame_time:
        boundaries.append(frame_time)

    intervals = zip(boundaries[:-1], boundaries[1:])
    assert len(intervals) > 0

    keyframes = []
    for start, stop in intervals:
        frame_num = int((start+stop) / 2.0 * video.tv.get_fps())
        timestamp = frame_num / video.tv.get_fps()

        frame = video.GetFrameNo(frame_num)

        # Find the hash of the representative image
        s = StringIO.StringIO()
        frame.save(s, 'JPEG')
        s.seek(0)
        imagehash = hashlib.md5(s.buf).hexdigest()

        # Store the image thumbnail itself
        frame = Image.open(s)
        frame.thumbnail((100,100))
        ts = StringIO.StringIO()
        frame.save(ts, 'JPEG')
        ts.seek(0)
        print 'keyframe: ' + imagehash
        yield ('frame', imagehash), ts.buf

        keyframes.append({
            'range': (start, stop),
            'frame_num': frame_num,
            'timestamp': timestamp,
            'image': {
                'hash': imagehash,
                'video': {'videohash': videohash, 'frame_num': frame_num},
                'faces': [],
                'categories': [],
                },
            'imagehash': imagehash,
            'children': [],
            })
    video = {
        'hash': videohash,
        'duration': video.tv.duration() / video.tv.get_fps(),
        'frames': video.tv.duration(),
        'fps': video.tv.get_fps(),
        'keyframes': keyframes
        }

    yield ('video', videohash), video
    yield ('scores', videohash), kf.scores


def mapper(videohash, video_data):

    video = pyffmpeg.VideoStream()
    videohash = hashlib.md5(video_data).hexdigest()
    print videohash
    with tempfile.NamedTemporaryFile(suffix='.avi') as fp:
        fp.write(video_data)
        fp.flush()
        video.open(fp.name)
        kf = keyframe.Histogram(skip_mod=5)
        #kf = keyframe.SURF(skip_mod=5)
        return keyframes(video, videohash, kf)


if __name__ == '__main__':
    hadoopy.run(mapper)
