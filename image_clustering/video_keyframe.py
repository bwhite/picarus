#!/usr/bin/env python
import pyffmpeg
import StringIO
import hashlib
import Image
import keyframe
import tempfile
import hadoopy
import os
import numpy as np
import vidfeat


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


def keyframes(iter1, iter2, videohash, kf, min_resolution, max_resolution):
    """
    Args:
        frame_iter_lambda: call this to get an iterator (must work twice)
        min_resolution: the maximum number of keyframes to display in a
                        cluster, controls the subdividing of clusters
        max_resolution: the minimum distance between keyframes, in seconds
    """
    # First pass
    # Find all the boundaries, including the first and last frame,
    # discarding tiny intervals (< max_resolution)
    boundaries = [0.0]
    for (frame_num, frame_time, frame), iskeyframe in kf(iter1):
        if iskeyframe:
            print 'keyframe', frame_num
            boundaries.append(frame_time)
    if boundaries[-1] < frame_time:
        boundaries.append(frame_time)

    # Get the video statistics from the output
    video_frames = frame_num
    video_fps = frame_num / frame_time
    video_duration = frame_time

    intervals = zip(boundaries[:-1], boundaries[1:])
    assert len(intervals) > 0

    keyframes = []

    # Second pass
    # Grab all the 'middle' frames
    frame_time = 0
    for start, stop in intervals:
        while frame_time < (start+stop)/2:
            frame_num, frame_time, frame = iter2.next()

        timestamp = frame_time

        # Find the hash of the representative image
        s = StringIO.StringIO()
        frame.save(s, 'JPEG')
        s.seek(0)
        imagehash = hashlib.md5(s.buf).hexdigest()
        yield ('frame', imagehash), s.buf

        # Store the image thumbnail itself
        frame = Image.open(s)
        frame.thumbnail((100,100))
        ts = StringIO.StringIO()
        frame.save(ts, 'JPEG')
        ts.seek(0)
        #print 'keyframe: ' + imagehash
        yield ('thumb', imagehash), ts.buf

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
        n_per_child = int(np.ceil(len(keyframes) / float(divisions)))
        divisions = int(np.ceil(len(keyframes) / n_per_child))
        children = []
        count = 0
        if divisions > 1:
            for i in range(divisions):
                child = subdivide(keyframes[i*n_per_child:(i+1)*n_per_child])
                count += child['count']
                children.append(child)
        if count == 0:
            count = 1

        key = keyframes[int(len(keyframes)/2)]
        return {
            'range': (keyframes[0]['range'][0], keyframes[-1]['range'][1]),
            'frame_num': key['frame_num'],
            'timestamp': key['timestamp'],
            'image': key['image'],
            'imagehash': key['imagehash'],
            'children': children,
            'count': count
            }

    video = {
        'hash': videohash,
        'duration': video_duration,
        'frames': video_frames,
        'fps': video_fps,
        'keyframes': [subdivide(keyframes)]
        }
    print 'video: ', videohash
    print 'total keyframes:', len(keyframes)
    print 'reported keyframes', video['keyframes'][0]['count']
    yield ('video', videohash), video
    yield ('scores', videohash), kf.scores


def mapper(videohash, metadata):
    print 'mapper', videohash

    #extension = metadata['extension']
    #if metadata.has_key('video_data'):
    #    video_data = metadata['video_data']

    video_data = metadata

    max_resolution = float(os.environ.setdefault('MAX_RESOLUTION', '3.0'))
    min_resolution = int(os.environ.setdefault('MIN_RESOLUTION', '8'))

    videohash = hashlib.md5(video_data).hexdigest()
    print videohash
    # FIXME use an actual filename instead of assuming .avi
    with tempfile.NamedTemporaryFile(suffix='.avi') as fp:
        fp.write(video_data)
        fp.flush()
        if 'USE_FFMPEG' in os.environ:
            video = pyffmpeg.VideoStream()
            video.open(fp.name)
            iter1 = vidfeat.convert_video(video, ('frameiterskip', keyframe.histogram.MODES, 5))
            iter2 = vidfeat.convert_video(video, ('frameiterskip', ['RGB'], 5))
        else:
            iter1 = vidfeat.convert_video_ffmpeg(video, ('frameiterskip', keyframe.histogram.MODES, 5), frozen=True)
            iter2 = vidfeat.convert_video_ffmpeg(video, ('frameiterskip', ['RGB'], 5), frozen=True)

        kf = keyframe.Histogram()
        return keyframes(iter1, iter2, videohash, kf, min_resolution, max_resolution)


if __name__ == '__main__':
    hadoopy.run(mapper)
