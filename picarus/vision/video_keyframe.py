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
import picarus


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
    for (frame_num, frame_time, frame), iskeyframe in kf(iter1()):
        if iskeyframe:
            print 'keyframe', frame_num
            boundaries.append(frame_time)

    if not 'frame_time' in locals() or frame_time == 0:
        print 'There were no frames in this video:', videohash
        return

    # Get the video statistics from the output
    video_frames = frame_num
    video_fps = frame_num / frame_time
    video_duration = frame_time

    if boundaries[-1] < video_duration:
        boundaries.append(video_duration)

    intervals = zip(boundaries[:-1], boundaries[1:])
    assert len(intervals) > 0

    keyframes = []

    # Second pass
    # Grab all the 'middle' frames
    frame_time = 0
    iter2 = iter2()
    iter2.next()
    for start, stop in intervals:
        frame_time = (start+stop)/2
        frame_num = video_fps * frame_time
        frame_num, frame_time, frame = iter2.send(frame_num)
        timestamp = frame_time

        # Find the hash of the representative image
        s = StringIO.StringIO()
        frame.save(s, 'JPEG')
        s.seek(0)
        imagehash = hashlib.md5(s.buf).hexdigest()
        yield ('frame', imagehash), s.buf

        if 0:
            # Store the image thumbnail itself
            frame = Image.open(s)
            frame.thumbnail((100,100))
            ts = StringIO.StringIO()
            frame.save(ts, 'JPEG')
            ts.seek(0)
            # print 'keyframe: ' + imagehash
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
    # FIXME use an actual filename instead of assuming .avi
    with tempfile.NamedTemporaryFile(suffix='.avi') as fp:
        fp.write(video_data)
        fp.flush()
        if not 'USE_FFMPEG' in os.environ:
            video = pyffmpeg.VideoStream()
            video.open(fp.name)
            iter1 = lambda : vidfeat.convert_video(video, ('frameiterskip', keyframe.histogram.MODES, 5))
            iter2 = lambda : vidfeat.convert_video(video, ('frameiterskip', ['RGB'], 5))
        else:
            iter1 = lambda : vidfeat.convert_video_ffmpeg(fp.name, ('frameiterskip', keyframe.histogram.MODES, 5), frozen=True)
            iter2 = lambda : vidfeat.convert_video_ffmpeg(fp.name, ('frameiterskip', ['RGB'], 5), frozen=True)

        kf = keyframe.Histogram()

        # Do this instead of 'return' in order to keep the tempfile around
        for k, v in  keyframes(iter1, iter2, videohash, kf, min_resolution, max_resolution):
            print k
            yield k, v


if __name__ == '__main__':
    hadoopy.run(mapper)
