set -e

RUN=5
NAME=amiller
REPORT_OUTPUT=out/video_keyframes/run-${RUN}/report

python cluster.py video_keyframe /user/brandyn/videos_small /user/${NAME}/out/video_keyframes/run-${RUN}/ 8 3.0 --ffmpeg
python cluster.py report_video_keyframe /user/${NAME}/out/video_keyframes/run-${RUN}/ ${REPORT_OUTPUT}/report_video.js --local_thumb_output ${REPORT_OUTPUT}/vid_t

echo "report = " > ${REPORT_OUTPUT}/sample_report.js
cat ${REPORT_OUTPUT}/report_video.js >> ${REPORT_OUTPUT}/sample_report.js
cp static_sample_report.html ${REPORT_OUTPUT}/
