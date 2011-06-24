RUN=2
NAME=amiller
#python cluster.py image_feature /user/brandyn/indoors /user/${NAME}/tp/image_classify/run-${RUN}/feat_indoors
#python cluster.py image_feature /user/brandyn/outdoors /user/${NAME}/tp/image_classify/run-${RUN}/feat_outdoors

#python cluster.py classifier_labels /user/brandyn/tp/image_classify/run-1/feat_indoors /user/brandyn/tp/image_classify/run-1/feat_outdoors /user/${NAME}/tp/image_classify/run-${RUN}/labels indoor_outdoor indoor_outdoor.pkl
#python cluster.py train_classifier /user/${NAME}/tp/image_classify/run-${RUN}/classifiers indoor_outdoor.pkl /user/brandyn/tp/image_classify/run-1/feat_indoors /user/brandyn/tp/image_classify/run-1/feat_outdoors
#python cluster.py predict_classifier /user/${NAME}/tp/image_classify/run-${RUN}/classifiers /user/${NAME}/tp/image_classify/run-${RUN}/predict /user/brandyn/tp/image_classify/run-1/feat_outdoors /user/brandyn/tp/image_classify/run-1/feat_indoors
#python cluster.py join_predictions /user/${NAME}/tp/image_classify/run-${RUN}/predict /user/${NAME}/tp/image_classify/run-${RUN}/predict_join /user/brandyn/indoors /user/brandyn/outdoors
python cluster.py report_categories /user/amiller/tp/image_classify/run-${RUN}/predict_join out/cluster/run-${RUN}/indoor_outdoor.js --local_thumb_output out/cluster/run-${RUN}/t
echo "report = " > out/cluster/run-${RUN}/sample_report.js
cat out/cluster/run-${RUN}/indoor_outdoor.js >> out/cluster/run-${RUN}/sample_report.js
cp static_sample_report.html out/cluster/run-${RUN}/
