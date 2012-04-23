#!/usr/bin/env python
import hadoopy
import tempfile
import cStringIO as StringIO
import Image
import sys
import viderator
import keyframe
import imfeat
import numpy as np
import os
import cv
import time
import cv2
import imfeat
import picarus._classifiers as classifiers
import picarus._file_parse as file_parse
import picarus._features as features
import contextlib
import cPickle as pickle


class Timer(object):

    def __init__(self):
        self.total_times = {}
        self.total_counts = {}
        self.timers = {}
        self.start_time = time.time()

    def start(self, timer):
        self.timers[timer] = time.time()

    def stop(self, timer):
        try:
            diff = time.time() - self.timers[timer]
        except KeyError:
            print('No such timer [%s]' % timer)
            return
        try:
            self.total_times[timer] += diff
            self.total_counts[timer] += 1
        except KeyError:
            self.total_times[timer] = diff
            self.total_counts[timer] = 1

    @contextlib.contextmanager
    def __call__(self, timer):
        self.start(timer)
        yield
        self.stop(timer)

    def __del__(self):
        print('Timers')
        total_time = time.time() - self.start_time
        total_covered_time = 0.
        for timer_name in self.timers:
            total_covered_time += self.total_times[timer_name]
            print('%s: %f / %d = %f' % (timer_name,
                                        self.total_times[timer_name], self.total_counts[timer_name],
                                        self.total_times[timer_name] / self.total_counts[timer_name]))
        print('Total Covered: %f' % total_covered_time)
        print('Total: %f' % total_time)


def _detect_faces(img, cascade):
    min_size = (20, 20)
    image_scale = 2
    haar_scale = 1.2
    min_neighbors = 2
    haar_flags = 0
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                                cv.Round(img.height / image_scale)), 8, 1)
    cv.Resize(img, small_img, cv.CV_INTER_LINEAR)
    cv.EqualizeHist(small_img, small_img)
    faces = cv.HaarDetectObjects(small_img, cascade,
                                 cv.CreateMemStorage(0),
                                 haar_scale, min_neighbors, haar_flags,
                                 min_size)
    return [((x * image_scale, y * image_scale,
              w * image_scale, h * image_scale), n)
            for (x, y, w, h), n in faces]


def _parse_height_width():
    try:
        image_width = image_height = int(os.environ['IMAGE_LENGTH'])
    except KeyError:
        image_width = int(os.environ['IMAGE_WIDTH'])
        image_height = int(os.environ['IMAGE_HEIGHT'])
    return image_height, image_width


def cv_to_jpg(img):
    fp = StringIO.StringIO()
    imfeat.convert_image(img, ['RGB']).save(fp, 'JPEG')
    fp.seek(0)
    return fp.read()


def plot_matches(image, matches, points0, points1, max_feat_width, color=(0, 255, 0)):
    height = int((max_feat_width / float(image.width)) * image.height)
    image = cv.fromarray(cv2.resize(np.asarray(cv.GetMat(image)), (max_feat_width, height)))
    for match in matches:
        point0 = points0[match[0]]
        point1 = points1[match[1]]
        cv.Line(image, (int(point0['x']), int(point0['y'])), (int(point1['x']), int(point1['y'])), color=color)
    return image


class Mapper(object):

    def __init__(self):
        self.output_images = int(os.environ.get('OUTPUT_IMAGES', 0))
        path = 'haarcascade_frontalface_default.xml'
        if os.path.exists(path):
            self.cascade = cv.Load(path)
        else:
            raise ValueError("Can't find .xml file!")
        classifier_name, classifier_ser = file_parse.load(os.environ['CLASSIFIERS_FN'])
        self._classifiers = [(classifier_name, classifiers.loads(classifier_ser))]
        self._feat = features.select_feature(os.environ['FEATURE'])
        self._image_height, self._image_width = _parse_height_width()
        self._max_frames = os.environ.get('MAX_FRAMES', float('inf'))
        self._block_size = os.environ.get('BLOCK_SIZE', 900)
        self._match_line_prob = os.environ.get('MATCH_LINE_PROB', 0)
        self._frame_output_prob = os.environ.get('FRAME_OUTPUT_PROB', 0)
        self.timer = Timer()

    def map(self, event_filename, video_data):
        """

        Args:
            event_filename: Tuple of (event, filename)
            video_data: Binary video data

        Yields:
            A tuple in the form of ((event, filename), features) where features is a dict

            frame_features: List of frame features
            file_size: Size in bytes

            where each frame feature is a dictionary of

            frame_time: Time in seconds
            frame_num: Frame number
            prev_frame_num: Previous frame number (useful if there is a frame skip)
            keyframe: Boolean True/False
            surf: List of surf points (see impoint)
            face_widths:
            face_heights:
            predictions: Dictionary of predictions
        """
        sys.stderr.write('In Raw:%s\n' % str(event_filename))
        print(event_filename)
        ext = '.' + event_filename[1].rsplit('.')[1]
        with tempfile.NamedTemporaryFile(suffix=ext) as fp:
            with self.timer('Writing video data'):
                fp.write(video_data)
                fp.flush()
            kf = keyframe.DecisionTree(min_interval=0)
            kf.load()
            prev_frame = None
            prev_frame_num = 0
            all_out = []
            sz = len(video_data)

            self.timer.start('KF')
            try:
                for (frame_num, frame_time, frame), iskeyframe in kf(viderator.frame_iter(fp.name,
                                                                                          frozen=True)):
                    hadoopy.counter('RawFeatures', 'NumFrames')
                    self.timer.stop('KF')
                    print(frame_time)
                    if frame_num > self._max_frames:
                        break
                    if frame_num % 100 == 0:
                        with self.timer('Computing face features'):
                            faces = _detect_faces(imfeat.convert_image(frame, [('opencv', 'gray', 8)]),
                                                  self.cascade)
                    else:
                        faces = {}
                    out = {'frame_time': frame_time, 'frame_num': frame_num,
                           'prev_frame_num': prev_frame_num, 'keyframe': iskeyframe,
                           'surf': kf.prev_vec['surf']}
                    if faces:  # If any faces
                        face_heights = np.array([x[0][3] for x in faces]) / float(frame.height)
                        face_widths = np.array([x[0][2] for x in faces]) / float(frame.width)
                        out['face_widths'] = face_widths
                        out['face_heights'] = face_heights
                    # Output the cur and previous frames if this is a keyframe
                    if iskeyframe and np.random.random() < self._frame_output_prob:
                            out['prev_frame'] = cv_to_jpg(prev_frame)
                            out['frame'] = cv_to_jpg(frame)
                    # Compute scene features
                    with self.timer('Computing scene classifier features'):
                        frame_res = cv.fromarray(cv2.resize(np.asarray(cv.GetMat(frame)), (self._image_width, self._image_height)))
                        feature = self._feat(frame_res)
                        out['predictions'] = dict((classifier_name, classifier.predict(feature))
                                                  for classifier_name, classifier in self._classifiers)
                    # Output JPEG with match lines from the SURF feature
                    if np.random.random() < self._match_line_prob and prev_frame:
                        out['surf_image'] = cv_to_jpg(plot_matches(prev_frame, kf.surf_debug['matches'], kf.surf_debug['points0'],
                                                                   kf.surf_debug['points1'], max_feat_width=kf.max_feat_width))
                    # Output data buffer
                    all_out.append(out)
                    if len(all_out) >= self._block_size:
                        with self.timer('Yield'):
                            yield event_filename, {'frame_features': all_out,
                                                   'file_size': sz}
                            all_out = []
                    prev_frame = frame
                    prev_frame_num = frame_num
                self.timer.start('KF')
            except viderator.FPSParseException:  # NOTE(brandyn): This will disregard videos with this error
                hadoopy.counter('SkippedVideos', 'FPSParseException')
                return
            if all_out:
                with self.timer('Yield'):
                    yield event_filename, {'frame_features': all_out,
                                           'file_size': sz}

if __name__ == '__main__':
    hadoopy.run(Mapper)
