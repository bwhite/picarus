#!/usr/bin/env python
import StringIO
import hashlib
import Image
import keyframe
import tempfile
import hadoopy
import os
import numpy as np
import viderator
import picarus


def keyframes(iter1, iter2, metadata, kf, resolution):
    """Keyframes / scene boundary detection. The algorithms finds salient
    boundary images that occur between meaningful scenes or shots. An even
    sampling of 'within-interval' are returned for each interval/scene.

    Args:
        iter1, iter2:
            keyframing requires two passes through the video,
            (1) in a format defined by keyframe algorithm (kf),
            (2) in PIL format for saving to jpeg
        metadata:
            a video record object
        kf:
            an instance of a keyframe object, like keyframe.Histogram or
            keyframe.SURF
        resolution:
            duration (in seconds) between within-interval frames

    Yields:
        pass
    """
    # (1) First pass
    # Find all the boundaries, including the first and last frame,
    # discarding tiny intervals (< max_resolution)
    videohash = metadata['sha1']

    # Include the very first frame as an interval bondary
    boundaries = [0.0]
    for (frame_num, frame_time, frame), iskeyframe in kf(iter1()):
        if iskeyframe:
            #print 'keyframe', frame_num, frame_time
            boundaries.append(frame_time)

    if not 'frame_time' in locals() or frame_time == 0:
        print 'There were no frames in this video:', videohash
        return

    # Get the video statistics from the final frame (any frame should do,
    # but this relies on correct reporting from iter1
    video_frames = frame_num
    video_fps = frame_num / frame_time
    video_duration = frame_time

    # Always add the final frame as a boundary
    if boundaries[-1] < video_duration:
        boundaries.append(video_duration)

    intervals = zip(boundaries[:-1], boundaries[1:])
    # print 'intervals', len(intervals)
    # print dict(video_frames=video_frames, video_fps=video_fps, video_duration=video_duration)
    assert len(intervals) > 0

    keyframes = []

    # (2) Second pass
    # Grab all the internal 'within-inverval' frames
    frame_time = 0
    iter2 = iter2()
    iter2.next()
    fskip = max(int(resolution * video_fps), 1)
    total_count = 0
    #print 'fskip', fskip
    for start, stop in intervals:
        children = []
        for fn in range(int(start*video_fps), int(stop*video_fps), fskip):
            frame_num, frame_time, frame = iter2.send(fn)

            # Find the hash of the image
            s = StringIO.StringIO()
            frame.save(s, 'JPEG')
            s.seek(0)
            imagehash = hashlib.md5(s.buf).hexdigest()
            yield ('frame', imagehash), {'source_video': imagehash,
                                         'frame_num': frame_num,
                                         'image_data': s.buf}
            timestamp = frame_time
            #print start, stop, frame_num, timestamp

            # Add within-interval frames (every <resolution> seconds)
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
        # Add the representative image (the middle frame)
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

    # Add the representative image for the video
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

    # Video metadata
    video = {
        'hash': videohash,
        'duration': video_duration,
        'frames': video_frames,
        'fps': video_fps,
        'keyframes': [topkey],
        'full_path': metadata['full_path']
        }
    print 'video: ', videohash
    #print 'total keyframes:', len(keyframes)
    #print 'reported keyframes', video['keyframes'][0]['count']
    #print video
    yield ('video', videohash), video
    yield ('scores', videohash), kf.scores


def mapper(videohash, metadata):
    print('videohash[%s]' % videohash)
    print('hdfs_path[%s]' % metadata['hdfs_path'])
    print 'mapper', videohash

    filename = 'hardcodedvideo.' + metadata['extension']
    #print filename, metadata.keys()
    try:
        picarus.io._record_to_file(metadata, filename)
    except IOError:
        hadoopy.counter('INPUT_ERROR', 'REMOTE READ FAILED')
        return

    min_interval = float(os.environ['MIN_INTERVAL'])
    resolution = float(os.environ['RESOLUTION'])
    try:
        iter1 = lambda : viderator.frame_iter(filename, frame_skip=5, frozen=True)
        iter2 = lambda : viderator.convert_video_ffmpeg(filename, frame_skip=5, frozen=True)

        kf = keyframe.Histogram(min_interval)

        # Do this instead of 'return' in order to keep the tempfile around
        try:
            for k, v in  keyframes(iter1, iter2, metadata, kf, resolution):
                #print 'yield', k
                yield k, v
        except:
            hadoopy.counter('INPUT_ERROR', 'VIDEO_READ_ERROR')
            return
    finally:
        os.remove(filename)

if __name__ == '__main__':
    hadoopy.run(mapper)
