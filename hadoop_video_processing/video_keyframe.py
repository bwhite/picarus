#!/usr/bin/env python
import pyffmpeg
import StringIO
import hashlib
import Image
import keyframe
import tempfile
import hadoopy
import os


class Seeker(object):
    """For frame_iters that don't support random seeking (i.e. streaming from
    ffmpeg cmd), this makes it easy to skip forward
    """
    def __init__(self, frame_iter):
        self.counter = 0
        self.frame_iter = frame_iter
        self.frame = frame_iter.next()

    def get_frame_num(self, frame_num):
        assert frame_num >= self.counter
        while frame_num > self.counter:
            self.frame = self.frame_iter.next()
        return self.frame


def keyframes(video, videohash, kf, min_resolution, max_resolution):
    """
    Args:
        min_resolution: the maximum number of keyframes to display in a
                        cluster, controls the subdividing of clusters
        max_resolution: the minimum distance between keyframes, in seconds
    """
    # First pass
    # Find all the boundaries, including the first and last frame,
    # discarding tiny intervals (< max_resolution)
    boundaries = [0.0]
    for (frame_num, frame_time, frame), iskeyframe in kf(video):
        if iskeyframe:
            print 'keyframe', frame_num
            boundaries.append(frame_time)
    if boundaries[-1] < frame_time:
        boundaries.append(frame_time)

    intervals = zip(boundaries[:-1], boundaries[1:])
    assert len(intervals) > 0

    keyframes = []

    # Second pass
    # Grab all the 'middle' frames
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
        #print 'keyframe: ' + imagehash
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

    # Recursively merge the key frames to create a tree
    def subdivide(keyframes):
        assert len(keyframes) > 0
        divisions = min(min_resolution, len(keyframes))
        children = []
        if divisions > 1:
            n_per_child = int(len(keyframes) / divisions)
            for i in range(divisions):
                children.append(subdivide(keyframes[i*n_per_child:(i+1)*n_per_child]))

        key = keyframes[int(len(keyframes)/2)]
        return {
            'range': (keyframes[0]['range'][0], keyframes[-1]['range'][1]),
            'frame_num': key['frame_num'],
            'timestamp': key['timestamp'],
            'image': key['image'],
            'imagehash': key['imagehash'],
            'children': children
            }

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
    print 'mapper', videohash
    max_resolution = float(os.environ.setdefault('MAX_RESOLUTION', '3.0'))
    min_resolution = int(os.environ.setdefault('MIN_RESOLUTION', '8'))

    video = pyffmpeg.VideoStream()
    videohash = hashlib.md5(video_data).hexdigest()
    print videohash
    with tempfile.NamedTemporaryFile(suffix='.avi') as fp:
        fp.write(video_data)
        fp.flush()
        video.open(fp.name)
        kf = keyframe.Histogram(skip_mod=5)
        #kf = keyframe.SURF(skip_mod=5)
        return keyframes(video, videohash, kf, min_resolution, max_resolution)


if __name__ == '__main__':
    hadoopy.run(mapper)
