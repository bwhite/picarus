VIDEO_DIR=/home/amiller/videos/
for x in $(ls $VIDEO_DIR)
do
    python video_keyframe.py $VIDEO_DIR/$x --imagedir vid_t/ --outfile videojs/$x.js
done
