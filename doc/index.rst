Picarus
================================================


..  toctree::
    :maxdepth: 2

Visit https://github.com/bwhite/picarus/ for the source.

About
---------------------------

Requirements
------------
Our projects

- hadoopy_: Cython based Hadoop library for Python.  Efficient, simple, and powerful.
- imfeat_: Image features (take image, produce feature vector) and support functions.
- classipy_: Classifiers using a simple standardized interface (supports scikit-learn_).
- distpy_: Distance metrics.
- impoint_: Image feature point detection and description.
- vidfeat_: Video features (take video, produce feature vector) and support functions.
- keyframe_: Video keyframe algorithms (take video, identify frame changes).

Third party

- Scipy_
- OpenCV_
- Hadoop_ (CDH_ recommended)

.. _Scipy: http://www.scipy.org
.. _OpenCV: http://opencv.willowgarage.com/wiki/
.. _CDH: http://www.cloudera.com/hadoop/
.. _Hadoop: http://hadoop.apache.org/
.. _hadoopy: https://github.com/bwhite/hadoopy
.. _imfeat: https://github.com/bwhite/imfeat
.. _classipy: https://github.com/bwhite/classipy
.. _distpy: https://github.com/bwhite/distpy
.. _impoint: https://github.com/bwhite/impoint
.. _vidfeat: https://github.com/bwhite/vidfeat
.. _keyframe: https://github.com/bwhite/keyframe
.. _scikit-learn: http://scikit-learn.org/stable/

Useful Tools (Optional)
---------------------------
Our projects (ordered by relevance)

- hadoopy_flow_: Hadoopy monkey patch library to perform automatic job-level parallelism.
- vision_data_: Library of computer vision dataset interfaces with standardized output formats.
- image_server_: Server that displays all images in the current directory as a website (very convenient on headless servers).
- static_server_: Server that allows static file access to the current directory.
- vision_results_: Library HTML and Javascript tools to display computer vision results.
- hadoop_log_: Tool to scrape Hadoop jobtracker logs and provide stderr output (simplifies debugging).
- pyram_: Tiny parameter optimization library (useful when tuning up algorithms).

.. _hadoopy_flow: https://github.com/bwhite/hadoopy_flow
.. _vision_data: https://github.com/bwhite/vision_data
.. _hadoop_log: https://github.com/bwhite/hadoop_log
.. _pyram: https://github.com/bwhite/pyram
.. _image_server: https://github.com/bwhite/image_server
.. _vision_results: https://github.com/bwhite/vision_results
.. _static_server: https://github.com/bwhite/static_server

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
