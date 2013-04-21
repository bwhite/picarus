Picarus
========


..  toctree::
    :maxdepth: 2

    index
    api
    app
    takeout
    examples


About
--------

Picarus is a Computer Vision web service and library for large-scale visual analysis.  Behind the scenes it uses Hadoop/HBase and the front end provides an easy to use REST interface and web app.  This is a broad project and is under active development, contact us if you are interested in using it or would like to take part in the development.  Visit https://github.com/bwhite/picarus/ for the source.

Who
---
Picarus is developed by `Dapper Vision, Inc. <http://dappervision.com>`_ (`Brandyn White <http://brandynwhite.com>`_ and `Andrew Miller <http://blog.soc1024.com/pages/about-andrew-miller>`_).  We are PhD students at UMD and UCF respectively and are interested in Computer Vision, Web-Scale Machine Learning, HCI, Cryptography, and Social Networks.

History
----------

Concept and Draft (2008)

- "Computer vision web service"

First usable implementation (2011)

- "The OpenCV for Big Data and Hadoop"

- "Mahout for visual data"

Focus expanded (2012)

- "Full-lifecycle CV web application"

- Crawl, annotate, execute, train, analyze, visualize

Philosophy
----------
::

        Picarus Web App           HBase scales big              Free Software for all
        Visual Analysis   Scan slices with high throughput   Large Scale Computer Vision
       Look in your data           Contiguous Rows                 As Apache Two  


::

       Hadoop's not easy                                        Privacy is key
   Abstraction lowers the bar                          What we don't know can't hurt you
      REST is for humans                                       Ignorance is safe


Capabilities: Algorithms
------------------------
Below is an incomplete list of the algorithms available, more detail is available in the API documentation below.

- Crawling: Flickr
- Annotation: Standalone or Mechanical Turk.  Several operating modes.
- Visualization: Thumbnails, Metadata, Exif, and Location
- Image features
- Classifier Training
- Binary Hash Function Learning
- Search Indexing

Requirements
------------
Our projects

- hadoopy_ (`doc <http://hadoopy.co>`_): Cython based Hadoop library for Python.  Efficient, simple, and powerful.
- picarus_takeout_: C/C++ module that contains the core picarus algorithms, separate so that it can be built as a standalone executable.
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
.. _picarus_takeout: https://github.com/bwhite/picarus_takeout
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


Roles: How Picarus fits in
---------------------------
Picarus is designed to be used in a variety of capacities from data warehouse, execution engine, web application, REST API, and algorithm factory; however, these are intended to be optional and the level of integration and involvement should be determined by the user.

Data Warehouse
^^^^^^^^^^^^^^
Picarus uses two data models: row access (i.e., table/row) and contiguous row slice access (i.e., table/startRow/stopRow).  Each row contains a columns of values.  Essentially any datastore that can be modeled in this form can be easily integrated in Picarus.  Picarus currently uses HBase as the primary datastore and Redis for metadata.  Picarus can be used effectively as a convenient way to interface with data as it provides a convenient server with authentication, user permissions, and sharing.

Execution Engine
^^^^^^^^^^^^^^^^
Processing occurs either at the web application level or on Hadoop depending on the job submitted.  No state is kept on the Picarus application servers, which allows multiple instances to be run on separate machines behind a load balancer (e.g., nginx, haproxy).  Hadoop is powerful but often difficult for new developers to work with.  Picarus provides a simple interface for Hadoop algorithms.

Algorithm Factory
^^^^^^^^^^^^^^^^^
New classifiers can be trained, search indexes built, and algorithms instantiated.  These can all be composed into fairly complex algorithms and executed using Picarus; however, there is no reason why after the algorithm is trained that it needs to be executed solely by the Picarus environment.  Consequently, we designed the system so that every algorithm can be 'taken out' as a config file and executed by a standalone binary (see the picarus_takeout project for details).  The 'takeout' functionality is implemented in standard C/C++ with as few (and optional) dependencies as possible to enable the broad compatibility.  What that means is that you can use Picarus after algorithm creation for execution or you can extract the algorithms and use them as you wish (e.g., mobile apps, compiled to javascript, offline applications).  

REST API
^^^^^^^^
The API is provided at a RESTful protocol following standard conventions where possible.  Some of the Picarus functionality, such as slice level access, is unique to Picarus and there don't exist common conventions; in these instances we attempted to be consistent and use the 'least surprising' solution.

Web Application
^^^^^^^^^^^^^^^^
The web interface is implemented using Backbone.js as a single page that provides access to Picarus through the same REST api described in this documentation.  The web application is designed to be modular, it is very easy to add a new page for specific funtionality that you may want.

Models
------------------
Picarus abstracts data analysis as a sequence of models with a defined flow from source data through them.  Each model describes how to instantiate it, what inputs it took (either other models or raw source data), what parameters it has, user notes/tags, and permissions (i.e., who can use/modify it).  The result is that given a column name (i.e., data stored for a specific image) we can determine exactly what process of steps occured to create it; moreover, this allows for natural utilization of pre-processed data, re-use of components, and parallel computation.  Models are immutable once created and this is enforced by their row encoding the hash of the model, input, and parameters which allows for verifying that the model has not been modified since its creation.  This is necessary to ensure consistency; moreover, the versions of each underlying module in use are stored in the model so that it is possible to manually determine if an incompatible change has been made which would necessitate reprocessing the data.

Examples of models are preprocessors (i.e., take source data, condition is based on specific rules), features (i.e., take processed image and produce a visual feature), classifiers (i.e., take a feature and produce a confidence value (binary) or a ranked list of classes (multi-class)), hashers (i.e., take feature and produce a binary hash code), and search indexes (i.e., take a binary hash code and produce a ranked result list).  Essentially, an output column in the images table corresponds to a row in the models table.
