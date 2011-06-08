import hadoopy
import time


def run(hdfs_input, hdfs_output):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'grab_first_frame.py', reducer=None)


def main():
    run('videos', 'output/video_frame_grab/%f/' % time.time())

main()
