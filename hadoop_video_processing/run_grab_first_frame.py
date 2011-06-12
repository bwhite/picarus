import hadoopy
import time

#grab_first_frame
def run(hdfs_input, hdfs_output):
    hadoopy.launch_frozen(hdfs_input, hdfs_output, 'grab_first_frame.py', reducer=None)


def main():
    # videos
    run('videos_small', 'output/video_frame_grab/%f/' % time.time())

main()
