import video_raw_features
import video_block_features
import sys
import hadoopy


class Mapper(object):

    def __init__(self):
        self.b = video_block_features.Mapper()
        self.r = video_raw_features.Mapper()

    def map(self, event_filename, video_data):
        hadoopy.counter('CombinedFeatures', 'DontHave')
        sys.stderr.write('%s\n' % str(event_filename))
        for event_filename, features in self.r.map(event_filename, video_data):
            sys.stderr.write('%s\n' % str(event_filename))
            for x in self.b.map(event_filename, features):
                yield x


if __name__ == '__main__':
    hadoopy.run(Mapper, video_block_features.Reducer)
