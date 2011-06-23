RUN=15
python cluster.py face_finder /user/brandyn/flickr /user/brandyn/tp/face_cluster/run-${RUN}/faces
python cluster.py image_feature /user/brandyn/tp/face_cluster/run-${RUN}/faces /user/brandyn/tp/face_cluster/run-${RUN}/feat --feature eigenface --image_length 64
python cluster.py sample /user/brandyn/tp/face_cluster/run-${RUN}/feat /user/brandyn/tp/face_cluster/run-${RUN}/clust0 40
python cluster.py kmeans /user/brandyn/tp/face_cluster/run-${RUN}/feat /user/brandyn/tp/face_cluster/run-${RUN}/clust0 /user/brandyn/tp/face_cluster/run-${RUN}/faces /user/brandyn/tp/face_cluster/run-${RUN}/ 40 20 20