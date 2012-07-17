#!/usr/bin/env python
import hadoopy
import numpy as np
import tempfile
import imfeat
import viderator
from picarus._importer import call_import
import os
import vidfeat
import cPickle as pickle


class Mapper(object):

    def __init__(self):
        self._feat = pickle.load(open(os.environ['FEATURE_FN']))
        if isinstance(self._feat, dict):
            self._feat = call_import(self._feat)
        self.frame_skip = 30
        self.max_outputs_per_video = float(os.environ.get('MAX_OUTPUTS_PER_VIDEO', float('inf')))
        self.max_frames_per_video = float(os.environ.get('MAX_FRAMES_PER_VIDEO', float('inf')))
        self.output_frame = int(os.environ.get('OUTPUT_FRAME', 1))
        self.remove_bars = imfeat.BlackBars()

    def map(self, event_filename, video_data):
        """
        Args:
            event_filename: Tuple of (event, filename)
            video_data: Binary video data

        Yields:
            A tuple in the form of ((event, filename, frame_num, frame_time), frame_data)
        """
        ext = '.' + event_filename[1].rsplit('.')[1]
        event, filename = event_filename
        out_count = 0
        with tempfile.NamedTemporaryFile(suffix=ext) as fp:
            fp.write(video_data)
            fp.flush()
            try:
                for frame_num, frame_time, frame in viderator.frame_iter(fp.name,
                                                                         frozen=True,
                                                                         frame_skip=self.frame_skip):
                    if frame_num >= self.max_frames_per_video:
                        break
                    frame_orig = frame
                    if self.remove_bars:
                        sz = self.remove_bars.find_bars(frame)
                        frame = frame[sz[0]:sz[1], sz[2]:sz[3], :]
                        if not frame.size:  # Empty
                            continue
                    if self._feat.predict(frame):
                        if self.output_frame:
                            yield (event, filename, frame_num, frame_time), imfeat.image_tostring(frame_orig, 'JPEG')
                        else:
                            yield (event, filename, frame_num, frame_time), ''
                        out_count += 1
                        if out_count >= self.max_outputs_per_video:
                            break
            except IOError:
                hadoopy.counter('PICARUS', 'CantProcessVideo')


def reducer(k, vs):
    for v in vs:
        yield k, v

if __name__ == '__main__':
    hadoopy.run(Mapper, reducer)
