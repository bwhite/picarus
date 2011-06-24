import hadoopy
import vidfeat
import time


if __name__ == '__main__':
    hdfs_input = '/user/brandyn/videos/'
    hdfs_output = 'output/ffmpeg_frame/%f/' % time.time()
    with vidfeat.freeze_ffmpeg() as f:
        hadoopy.launch_frozen(hdfs_input, hdfs_output,
                             'ffmpeg_first_frame.py',
                              reducer=False,
                              files=(f),
                              jobconfs=['mapred.child.java.opts=-Xmx512M'])
