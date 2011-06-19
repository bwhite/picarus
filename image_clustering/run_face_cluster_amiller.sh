RUN=15
NAME=amiller
REPORT_OUTPUT=out/face_cluster/run-${RUN}/report

#python cluster.py face_finder /user/brandyn/flickr /user/brandyn/tp/face_cluster/run-${RUN}/faces
#python cluster.py image_feature /user/brandyn/tp/face_cluster/run-${RUN}/faces /user/brandyn/tp/face_cluster/run-${RUN}/feat --feature eigenface --image_length 64
#python cluster.py sample /user/brandyn/tp/face_cluster/run-${RUN}/feat /user/${NAME}/tp/face_cluster/run-${RUN}/clust0 40
#python cluster.py kmeans /user/brandyn/tp/face_cluster/run-${RUN}/feat /user/${NAME}/tp/face_cluster/run-${RUN}/clust0 /user/brandyn/tp/face_cluster/run-${RUN}/faces /user/${NAME}/tp/face_cluster/run-${RUN}/ 40 20 20
#python cluster.py report_thumbnails /user/brandyn/tp/face_cluster/run-${RUN}/faces out/face_cluster/run-${RUN}/report/face_t/
python cluster.py report_clusters /user/${NAME}/tp/face_cluster/run-${RUN}/samples ${REPORT_OUTPUT}/report_cluster.js faces --sample 200

echo "report = " > ${REPORT_OUTPUT}/sample_report.js
cat ${REPORT_OUTPUT}/report_cluster.js >> ${REPORT_OUTPUT}/sample_report.js
cp static_sample_report.html ${REPORT_OUTPUT}/
