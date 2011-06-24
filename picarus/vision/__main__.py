import hadoopy
import vidfeat
import os


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def run_image_feature(hdfs_input, hdfs_output, feature, image_length, **kw):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, _lf('feature_compute.py'), reducer=False,
                          cmdenvs=['IMAGE_LENGTH=%d' % image_length,
                                   'FEATURE=%s' % feature],
                          files=[_lf('data/eigenfaces_lfw_cropped.pkl')])


def run_face_finder(hdfs_input, hdfs_output, image_length, boxes, **kw):
    cmdenvs = ['IMAGE_LENGTH=%d' % image_length]
    if boxes:
        cmdenvs.append('OUTPUT_BOXES=True')
    hadoopy.launch_frozen(hdfs_input, hdfs_output, _lf('face_finder.py'), reducer=False,
                          cmdenvs=cmdenvs,
                          files=[_lf('data/haarcascade_frontalface_default.xml')])


def run_video_keyframe(hdfs_input, hdfs_output, min_resolution, max_resolution, ffmpeg, **kw):
    if not ffmpeg:
        hadoopy.launch_frozen(hdfs_input, hdfs_output, _lf('video_keyframe.py'),
                              reducer=None,
                              cmdenvs=['MIN_RESOLUTION=%d' % min_resolution,
                                       'MAX_RESOLUTION=%f' % max_resolution])
    else:
        fp = vidfeat.freeze_ffmpeg()
        hadoopy.launch_local(hdfs_input, hdfs_output, _lf('video_keyframe.py'),
                              reducer=None,
                              cmdenvs=['MIN_RESOLUTION=%d' % min_resolution,
                                       'MAX_RESOLUTION=%f' % max_resolution,
                                       'USE_FFMPEG=1'],
                              files=fp.__enter__(),
                              dummy_arg=fp)
    hadoopy.launch_local(hdfs_output, hdfs_output + '/keyframes', _lf('video_keyframe_collect.py'),
                      reducer=None)
