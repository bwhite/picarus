import hadoopy
import vidfeat
import os
import picarus
import glob
import tempfile
from picarus import _file_parse as file_parse


def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def _parser(sps):
    import picarus.__main__
    ca = picarus.__main__._ca

    # Image Feature
    s = sps.add_parser('image_feature', help='Compute features on entire image')
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('--feature', **ca['feature'])
    s.add_argument('--image_length', **ca['image_length'])
    s.add_argument('hdfs_input', nargs='+', **ca['input'])
    s.set_defaults(func=picarus.vision.run_image_feature)

    # Face Finder
    s = sps.add_parser('face_finder', help='Extract faces')
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('--image_length', **ca['image_length'])
    s.add_argument('--boxes', help='If True make the value (image_data, boxes) where boxes is a list of (x, y, h, w)', type=bool, default=False)
    s.add_argument('hdfs_input', nargs='+', **ca['input'])
    s.set_defaults(func=picarus.vision.run_face_finder)

    # Run Video Keyframing
    s = sps.add_parser('video_keyframe', help='Run Video Keyframing')
    s.add_argument('hdfs_output', **ca['output'])
    s.add_argument('min_interval', type=float, help='Minimum duration (seconds) between keyframes')
    s.add_argument('--resolution', type=float, help='Duration (seconds) between output frames (default: all frames)', default=0.0)
    s.add_argument('--ffmpeg', help='Use frozen ffmpeg binary instead of pyffmpeg (works with more kinds of encoded videos, poorly enocded videos)', action='store_true')
    s.add_argument('hdfs_input', nargs='+', **ca['input'])
    s.set_defaults(func=picarus.vision.run_video_keyframe)


def run_image_feature(hdfs_input, hdfs_output, feature, image_length=None, image_height=None, image_width=None, **kw):
    if image_length:
        image_height = image_width = image_length
    picarus._launch_frozen(hdfs_input, hdfs_output, _lf('feature_compute.py'),
                           cmdenvs=['IMAGE_HEIGHT=%d' % image_height,
                                    'IMAGE_WIDTH=%d' % image_width,
                                    'FEATURE=%s' % feature],
                           files=[_lf('data/eigenfaces_lfw_cropped.pkl')])


def run_face_finder(hdfs_input, hdfs_output, image_length, boxes, **kw):
    cmdenvs = ['IMAGE_LENGTH=%d' % image_length]
    if boxes:
        cmdenvs.append('OUTPUT_BOXES=True')
    picarus._launch_frozen(hdfs_input, hdfs_output, _lf('face_finder.py'), reducer=None,
                           cmdenvs=cmdenvs,
                           files=[_lf('data/haarcascade_frontalface_default.xml')])


def run_predict_windows(hdfs_input, hdfs_classifier_input, feature, hdfs_output, image_height, image_width, **kw):
    import classipy
    # NOTE: Adds necessary files
    files = glob.glob(classipy.__path__[0] + "/lib/*")
    fp = tempfile.NamedTemporaryFile(suffix='.pkl.gz')
    file_parse.dump(list(hadoopy.readtb(hdfs_classifier_input)), fp.name)
    files.append(fp.name)
    files.append(_lf('data/haarcascade_frontalface_default.xml'))
    cmdenvs = ['CLASSIFIERS_FN=%s' % os.path.basename(fp.name)]
    cmdenvs += ['IMAGE_HEIGHT=%d' % image_height,
                'IMAGE_WIDTH=%d' % image_width,
                'FEATURE=%s' % feature]
    picarus._launch_frozen(hdfs_input, hdfs_output, _lf('predict_windows.py'),
                           cmdenvs=cmdenvs,
                           files=files,
                           jobconfs=['mapred.child.java.opts=-Xmx1024M'],
                           dummy_arg=fp)


def run_video_keyframe(hdfs_input, hdfs_output, min_interval, resolution, ffmpeg, **kw):

    if not ffmpeg:
        picarus._launch_frozen(hdfs_input, hdfs_output + '/keyframe', _lf('video_keyframe.py'),
                               reducer=None,
                               cmdenvs=[
                                   'MIN_INTERVAL=%f' % min_interval,
                                   'RESOLUTION=%f' % resolution],
                               jobconfs=['mapred.child.java.opts=-Xmx512M'],
                               )
    else:
        fp = vidfeat.freeze_ffmpeg()
        picarus._launch_frozen(hdfs_input, hdfs_output + '/keyframe', _lf('video_keyframe.py'),
                               reducer=None,
                               cmdenvs=[
                                   'MIN_INTERVAL=%f' % min_interval,
                                   'RESOLUTION=%f' % resolution,
                                   'USE_FFMPEG=1'],
                               files=fp.__enter__(),
                               jobconfs=['mapred.child.java.opts=-Xmx512M'],
                               dummy_arg=fp)

    picarus._launch_frozen(hdfs_output + '/keyframe', hdfs_output + '/allframes', _lf('video_keyframe_filter.py'),
                      reducer=None)
