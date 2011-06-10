RUN=4
python cluster.py image_feature /user/brandyn/flickr /user/brandyn/tp/image_cluster/run-${RUN}/feat
python cluster.py sample /user/brandyn/tp/image_cluster/run-${RUN}/feat /user/brandyn/tp/image_cluster/run-${RUN}/clust0 20
python cluster.py kmeans /user/brandyn/tp/image_cluster/run-${RUN}/feat /user/brandyn/tp/image_cluster/run-${RUN}/clust0 /user/brandyn/flickr /user/brandyn/tp/image_cluster/run-${RUN}/ 20 5 20