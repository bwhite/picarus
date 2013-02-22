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

Background
----------

- Concept and Draft (2008)
-- "Computer vision web service"
- First usable implementation (2011)
-- "The OpenCV for Big Data and Hadoop"
-- "Mahout for visual data"
- Focus expanded (2012)
-- "Full-lifecycle CV web application"
-- Crawl, annotate, execute, train, analyze, visualize

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

All calls use HTTP Basic Authentication with an email as the user and either the Login Key (only for /auth/) or API Key (everything but /auth/) as the password.

* Email: Used to send API/Login keys, used in all calls as the "user".
* Login Key: Used only for /auth/ calls as they are used to get an API key.
* API Key: Used for all other calls.

Get an API Key (email)
^^^^^^^^^^^^^^^^^^^^^^^
Send user an email with an API key.

RESOURCE URL
""""""""""""
POST https://api.picar.us/a1/auth/email

PARAMETERS
"""""""""""
None

EXAMPLE RESPONSE
""""""""""""""""
.. code:: javascript

    {}

Get an API Key (yubikey)
^^^^^^^^^^^^^^^^^^^^^^^
Return an API Key given a Yubikey One-Time Password (OTP).

RESOURCE URL
""""""""""""
POST https://api.picar.us/a1/auth/yubikey

PARAMETERS
"""""""""""
otp (string): Yubikey token

EXAMPLE RESPONSE
""""""""""""""""
.. code:: javascript

    {"apiKey": "w0tnnb7wcUbpZFp8wH57"}


Row Manipulation (/data)
---------------------------
CREATE |arrow| POST /:table  - Create new row, generating row key using user's upload prefix

READ |arrow| GET /:table/:row  - Get row

UPDATE |arrow| PATCH /:table/:row  - Modify attributes on an row, row/columns need not exist before hand (can be used to create)

DELETE |arrow| DELETE /:table/:row - Delete a row (idempotent)

DELETE |arrow| DELETE /:table/:row/:column - Delete a column from a row (idempotent)

EXECUTE |arrow| POST /:table/:row - ?(action)

Slice Manipulation (/slice)
---------------------------
READ |arrow| GET /:table/:startRow/:stopRow  - Get a row slice (TODO, params)

EXECUTE |arrow| POST /:table/:startRow/:stopRow - ?(action)


.. |arrow| unicode:: U+2794 .. right arrow

+---------+----------------------------------+-----------+---------+
| VERB    |  PATH                            |  Images   | Models  |
+---------+----------------------------------+-----------+---------+
| GET     | /data/:table                     | N         | Y       |
+---------+----------------------------------+-----------+---------+
| GET     | /slice/:table/:startRow/:stopRow | Y         | N       |
+---------+----------------------------------+-----------+---------+
| GET     | /data/:table/:row                | Y         | Y       |
+---------+----------------------------------+-----------+---------+
| POST    | /data/:table                     | Y         | N       |
+---------+----------------------------------+-----------+---------+
| POST    | /data/:table/:row                | Y         | N       |
+---------+----------------------------------+-----------+---------+
| POST    | /slice/:table/:startRow/:stopRow | Y         | N       |
+---------+----------------------------------+-----------+---------+
| PATCH   | /data/:table/:row                | Y\*       | Y\*     |
+---------+----------------------------------+-----------+---------+
| DELETE  | /data/:table/:row                | Y         | Y       |
+---------+----------------------------------+-----------+---------+
| DELETE  | /data/:table/:row/:column        | Y         | Y       |
+---------+----------------------------------+-----------+---------+
| DELETE  | /slice/:table/:startRow/:stopRow | TODO      | N       |
+---------+----------------------------------+-----------+---------+

Uploading an image
^^^^^^^^^^^^^^^^^^
Upload an image without specifying a row.

RESOURCE URL
""""""""""""
POST https://api.picar.us/a1/data/:table

table: (string) name of the table (e.g., images)

PARAMETERS
"""""""""""
\*ub64 column\* (ub64): binary



EXAMPLE RESPONSE
""""""""""""""""
.. code:: javascript

    {"row": ub64 row}


HBase
======

Images Table (images)
---------------------

Row
^^^
Each row corresponds to an "image" along with all associated features, metadata, etc.

Permissions
^^^^^^^^^^^
TODO

Column Families
^^^^^^^^^^^^^^^

data
"""""
Image data.

data:image is where the "source" image goes.  Preprocessors place other copies in data:

thum
""""
Where visualization-only thumbnails exist (these are not to be used for actual analysis)

image_150sq is an image with all sides equal to 150, cropping excess.

feat
""""
Image features (picarus.api.NDArray vector, fixed size)

mfeat
"""""
Image features (picarus.api.NDArray matrix, fixed columns, variable rows)

mask
""""
Image masks (picarus.api.NDArray matrix, height/width matching image, fixed depth)

pred
""""
Image predictions stored as a binary double.

srch
""""
Search results

attr
""""
Image attributes (basically metadata that is derived from the source data).  Similar to a prediction but generally "higher level", may come form a human and should generally be standardized.

hash
""""
Hash codes stored as binary bytes.  Separated from feat so that it can be scanned fast.

meta
""""
Image labels, tags, etc.

misc
""""
Columns that don't fit into the other categories.

Models Table
------------

Permissions
^^^^^^^^^^^
TODO

Row
^^^
Each row corresponds to a "model" which is something derived from data, primarily from the images table.  Parameters of the model should be included, along with the source columns used to produce it.

Column Families
^^^^^^^^^^^^^^^^

data
""""
Used for all data.
