RUN=1
#python cluster.py image_feature /user/brandyn/indoors /user/brandyn/tp/image_classify/run-${RUN}/feat_indoors
#python cluster.py image_feature /user/brandyn/outdoors /user/brandyn/tp/image_classify/run-${RUN}/feat_outdoors
#python cluster.py classifier_labels /user/brandyn/tp/image_classify/run-${RUN}/feat_indoors /user/brandyn/tp/image_classify/run-${RUN}/feat_outdoors /user/brandyn/tp/image_classify/run-${RUN}/labels indoor_outdoor indoor_outdoor.pkl
#python cluster.py train_classifier /user/brandyn/tp/image_classify/run-${RUN}/classifiers indoor_outdoor.pkl /user/brandyn/tp/image_classify/run-${RUN}/feat_indoors /user/brandyn/tp/image_classify/run-${RUN}/feat_outdoors
python cluster.py predict_classifier /user/brandyn/tp/image_classify/run-${RUN}/classifiers /user/brandyn/tp/image_classify/run-${RUN}/predict /user/brandyn/tp/image_classify/run-${RUN}/feat_outdoors /user/brandyn/tp/image_classify/run-${RUN}/feat_indoors
