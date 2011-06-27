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


def keyframes(iter1, iter2, metadata, kf, max_resolution):
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
    videohash = metadata['sha1']
    boundaries = [0.0]
    for (frame_num, frame_time, frame), iskeyframe in kf(iter1()):
        if iskeyframe:
            print 'keyframe', frame_num, frame_time
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
    fskip = max(int(max_resolution * video_fps), 1)
    total_count = 0
    for start, stop in intervals:
        children = []
        for fn in range(int(start*video_fps), int(stop*video_fps), fskip):
            frame_num, frame_time, frame = iter2.send(fn)

            # Find the hash of the representative image
            s = StringIO.StringIO()
            frame.save(s, 'JPEG')
            s.seek(0)
            imagehash = hashlib.md5(s.buf).hexdigest()
            yield ('frame', imagehash), s.buf
            timestamp = frame_time

            children.append({
                'range': (timestamp, timestamp),
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
                'count': 1
                })
        key = children[len(children)/2]
        keyframes.append({
            'range': (start, stop),
            'frame_num': key['frame_num'],
            'timestamp': key['timestamp'],
            'image': key['image'],
            'imagehash': key['imagehash'],
            'children': children,
            'count': len(children),
            })
        total_count += len(children)

    key = keyframes[len(keyframes)/2]
    topkey = {
        'range': (0, video_duration),
        'frame_num': key['frame_num'],
        'timestamp': key['timestamp'],
        'image': key['image'],
        'imagehash': key['imagehash'],
        'children': keyframes,
        'count': total_count,
        }

    video = {
        'hash': videohash,
        'duration': video_duration,
        'frames': video_frames,
        'fps': video_fps,
        'keyframes': [topkey],
        'full_path': metadata['full_path']
        }
    print 'video: ', videohash
    print 'total keyframes:', len(keyframes)
    print 'reported keyframes', video['keyframes'][0]['count']
    yield ('video', videohash), video
    yield ('scores', videohash), kf.scores


def mapper(videohash, metadata):
    print 'mapper', videohash

    filename = 'hardcodedvideo' + metadata['extension']
    picarus.io._record_to_file(metadata, filename)

    max_resolution = float(os.environ['MAX_RESOLUTION'])
    try:
        # FIXME use an actual filename instead of assuming .avi
        if not 'USE_FFMPEG' in os.environ:
            video = pyffmpeg.VideoStream()
            video.open(filename)
            iter1 = lambda : vidfeat.convert_video(video, ('frameiterskip', keyframe.histogram.MODES, 5))
            iter2 = lambda : vidfeat.convert_video(video, ('frameiterskip', ['RGB'], 5))
        else:
            iter1 = lambda : vidfeat.convert_video_ffmpeg(filename, ('frameiterskip', keyframe.histogram.MODES, 5), frozen=True)
            iter2 = lambda : vidfeat.convert_video_ffmpeg(filename, ('frameiterskip', ['RGB'], 5), frozen=True)

        kf = keyframe.Histogram()

        # Do this instead of 'return' in order to keep the tempfile around
        for k, v in  keyframes(iter1, iter2, metadata, kf, max_resolution):
            yield k, v
    finally:
        os.remove(filename)

if __name__ == '__main__':
    hadoopy.run(mapper)
