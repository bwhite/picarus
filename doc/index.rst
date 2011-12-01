Picarus
================================================


..  toctree::
    :maxdepth: 2

Visit https://github.com/bwhite/imfeat/ for the source.

About
---------------------------

Hadoop Vision Jobs
------------------
..  autofunction:: picarus.vision.run_image_feature
..  autofunction:: picarus.vision.run_video_keyframe
..  autofunction:: picarus.vision.run_predict_windows

Hadoop Cluster Jobs
-------------------
..  autofunction:: picarus.cluster.run_whiten
..  autofunction:: picarus.cluster.run_sample
..  autofunction:: picarus.cluster.run_kmeans
..  autofunction:: picarus.cluster.run_hac
..  autofunction:: picarus.cluster.run_local_kmeans

Hadoop Classification Jobs
--------------------------
..  autofunction:: picarus.classify.run_classifier_labels
..  autofunction:: picarus.classify.run_train_classifier
..  autofunction:: picarus.classify.run_predict_classifier
..  autofunction:: picarus.classify.run_join_predictions
..  autofunction:: picarus.classify.run_thresh_predictions


Hadoop IO
--------------------------
..  autofunction:: picarus.io.load_local
..  autofunction:: picarus.io.dump_local
..  autofunction:: picarus.io.run_record_to_kv
..  autofunction:: picarus.io.run_kv_to_record
