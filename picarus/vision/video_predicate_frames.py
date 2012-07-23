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
        self._feats = pickle.load(open(os.environ['FEATURES_FN']))
        self._feats = [call_import(x) if isinstance(x, dict) else x
                       for x in self._feats]
        self.frame_skip = 30
        self.max_frames_per_video = float(os.environ.get('MAX_FRAMES_PER_VIDEO', float('inf')))
        self.remove_bars = imfeat.BlackBars()

    def map(self, event_filename, video_data):
        """
        Args:
            event_filename: Tuple of (event, filename)
            video_data: Binary video data

        Yields:
            A tuple in the form of (event, (filename, array)) where
            array is F x (P + 2) where P is the number of predicates, F
            is the number of frames.  The last two columns are frame_num
            and frame_time.
        """
        ext = '.' + event_filename[1].rsplit('.')[1]
        event, filename = event_filename
        out = []
        with tempfile.NamedTemporaryFile(suffix=ext) as fp:
            fp.write(video_data)
            fp.flush()
            try:
                for frame_num, frame_time, frame in viderator.frame_iter(fp.name,
                                                                         frozen=True,
                                                                         frame_skip=self.frame_skip):
                    if frame_num >= self.max_frames_per_video:
                        break
                    if self.remove_bars:
                        sz = self.remove_bars.find_bars(frame)
                        frame = frame[sz[0]:sz[1], sz[2]:sz[3], :]
                    out.append([x.predict(frame) for x in self._feats] + [frame_num, frame_time])
            except IOError:
                hadoopy.counter('PICARUS', 'CantProcessVideo')
                hadoopy.counter('SkippingTaskCounters', 'MapProcessedRecords')
                return
        yield event, (filename, np.asfarray(out))
        hadoopy.counter('SkippingTaskCounters', 'MapProcessedRecords')


def reducer(event, filename_predicates):
    yield event, dict(filename_predicates)
    hadoopy.counter('SkippingTaskCounters', 'ReduceProcessedGroups')

if __name__ == '__main__':
    hadoopy.run(Mapper, reducer)
