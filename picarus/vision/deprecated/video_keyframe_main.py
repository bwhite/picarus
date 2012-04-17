# removed from __main__.py
def run_video_keyframe(hdfs_input, hdfs_output, min_interval, resolution, ffmpeg, **kw):

    if not ffmpeg:
        picarus._launch_frozen(hdfs_input, hdfs_output + '/keyframe', _lf('video_keyframe.py'),
                               reducer=None,
                               cmdenvs=['MIN_INTERVAL=%f' % min_interval,
                                        'RESOLUTION=%f' % resolution])
    else:
        fp = viderator.freeze_ffmpeg()
        picarus._launch_frozen(hdfs_input, hdfs_output + '/keyframe', _lf('video_keyframe.py'),
                               reducer=None,
                               cmdenvs=['MIN_INTERVAL=%f' % min_interval,
                                        'RESOLUTION=%f' % resolution,
                                        'USE_FFMPEG=1'],
                               files=[fp.__enter__()],
                               dummy_arg=fp)

    picarus._launch_frozen(hdfs_output + '/keyframe', hdfs_output + '/allframes', _lf('video_keyframe_filter.py'),
                           reducer=None)

