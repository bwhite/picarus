set -e

RUN=6
NAME=amiller
REPORT_OUTPUT=out/image_cluster/run-${RUN}/report

#python cluster.py image_feature /user/brandyn/flickr /user/brandyn/tp/${NAME}/run-${RUN}/feat
#python cluster.py sample /user/brandyn/tp/image_cluster/run-${RUN}/feat /user/${NAME}/tp/image_cluster/run-${RUN}/clust0 20
#python cluster.py kmeans /user/brandyn/tp/image_cluster/run-${RUN}/feat /user/${NAME}/tp/image_cluster/run-${RUN}/clust0 /user/brandyn/flickr /user/${NAME}/tp/image_cluster/run-${RUN}/ 20 5 20

#python cluster.py report_thumbnails /user/brandyn/flickr out/image_cluster/run-${RUN}/report/t/
python cluster.py report_clusters /user/brandyn/tp/image_cluster/run-${RUN}/samples ${REPORT_OUTPUT}/report_cluster.js indoor

echo "report = " > ${REPORT_OUTPUT}/sample_report.js
cat ${REPORT_OUTPUT}/report_cluster.js >> ${REPORT_OUTPUT}/sample_report.js
cp static_sample_report.html ${REPORT_OUTPUT}/
