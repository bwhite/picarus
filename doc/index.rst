Picarus
========


..  toctree::
    :maxdepth: 2

Visit https://github.com/bwhite/picarus/ for the source.

About
--------

Who
---
Picarus is developed by `Dapper Vision, Inc. <http://dappervision.com>`_ (`Brandyn White <http://brandynwhite.com>`_ and `Andrew Miller <http://blog.soc1024.com/pages/about-andrew-miller>`_).  We are PhD students at UMD and UCF respectively and are interested in Computer Vision, Web-Scale Machine Learning, HCI, Cryptography, and Social Networks.

Philosophy
----------

Capabilities
------------
Data Management

- Crawling: Flickr
- Annotation: Standalone or Mechanical Turk.  Several operating modes.

Visualization

- Thumbnails:
- Metadata:
- Exif:
- Location: 

Computer Vision

- Image features:

Machine Learning

- Classifier Learning:

Image Search

- Binary Hash Function Learning: 
- Search Indexing: 

Security
--------

Authentication

Permissions

Requirements
------------
Our projects

- hadoopy_ (`doc <http://hadoopy.co>`_): Cython based Hadoop library for Python.  Efficient, simple, and powerful.
- imfeat_ (`doc <http://bwhite.github.com/imfeat/>`_): Image features (take image, produce feature vector) and support functions.
- distpy_ (`doc <http://bwhite.github.com/distpy/>`_): Distance metrics.
- classipy_: Classifiers using a simple standardized interface (supports scikit-learn_).
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
- pycassa_server_: Pycassa viewer.
- vision_results_: Library HTML and Javascript tools to display computer vision results.
- hadoop_log_: Tool to scrape Hadoop jobtracker logs and provide stderr output (simplifies debugging).
- pyram_: Tiny parameter optimization library (useful when tuning up algorithms).
- mturk_vision_: Mechanical turk scripts.

.. _hadoopy_flow: https://github.com/bwhite/hadoopy_flow
.. _vision_data: https://github.com/bwhite/vision_data
.. _hadoop_log: https://github.com/bwhite/hadoop_log
.. _pyram: https://github.com/bwhite/pyram
.. _image_server: https://github.com/bwhite/image_server
.. _vision_results: https://github.com/bwhite/vision_results
.. _static_server: https://github.com/bwhite/static_server
.. _mturk_vision: https://github.com/bwhite/mturk_vision
.. _pycassa_server: https://github.com/bwhite/pycassa_server


API
===


Authentication
--------------


Row Manipulation (/data)
---------------------------
CREATE U+02794 POST /:table  - Create new row, generating row key using user's upload prefix
READ U+02794 GET /:table/:row  - Get row
UPDATE U+02794 PATCH /:table/:row  - Modify attributes on an row, row/columns need not exist before hand (can be used to create)
DELETE U+02794 DELETE /:table/:row - Delete a row (idempotent)
DELETE U+02794 DELETE /:table/:row/:column - Delete a column from a row (idempotent)
EXECUTE U+02794 POST /:table/:row - ?(action)

Slice Manipulation (/slice)
---------------------------
READ U+02794 GET /:table/:startRow/:stopRow  - Get a row slice (TODO, params)
EXECUTE U+02794 POST /:table/:startRow/:stopRow - ?(action)
