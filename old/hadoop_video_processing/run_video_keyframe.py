import hadoopy
import time


def run(hdfs_input, hdfs_output):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'video_keyframe.py',
                          reducer=None)


def run_local(hdfs_input, hdfs_output):
    hadoopy.launch_local(hdfs_input, hdfs_output, 'video_keyframe.py',
                         reducer=None)


def main():
    # videos
    run('/user/brandyn/videos_small',
        'output/video_keyframes/%f/' % time.time())

main()
