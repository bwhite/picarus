Picarus
========

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


Capabilities
------------
Below is an incomplete list, more detail is available in the API documentation below.

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

API Overview
--------------
You can access data by row (/data/:table/:row) or by slice (/slice/:table/:startRow/:stopRow which is [startRow, stopRow)).  Slices exploit the contiguous nature of the rows in HBase and allow for batch execution on Hadoop.  

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
* otp (string): Yubikey token

EXAMPLE RESPONSE
""""""""""""""""
.. code:: javascript

    {"apiKey": "w0tnnb7wcUbpZFp8wH57"}

Encodings
---------
JSON has become the standard interchange for REST services; however, it does not support binary data without encoding and when using HBase the row/column/value is, in general, binary as the underlying data is a byte string.  Moreover, we often using rows/columns in URLs, making standard url escape (due to %00 primarily) and base64 not appropriate as various browsers and intermediate servers will have issues with URLs containing these characters.  Values on the other hand are never used in URLs but they still must be JSON safe.  Base64 encoding is often performed natively and as values are often large (much larger than rows/columns) it makes sense to ensure that encoding/decoding them is as efficient as possible.  Consequently, rows/columns are always "urlsafe" base64 (+ -> - and / -> _) and values are always base64.  Below are implementations of the necessary enc/dec functions for all the encodings necessary in Picarus.  The encodings will be referred to by their abbreviated name (e.g., ub64) and from context it will be clear if enc/dec is intended.


Python
^^^^^^
.. code-block:: python

    import base64
    import json

    # b64
    b64_enc = base64.b64encode
    b64_dec = base64.b64decode

    # ub64
    ub64_enc = base64.urlsafe_b64encode
    ub64_dec = base64.urlsafe_b64decode

    # json_ub64_b64
    json_ub64_b64_enc = lambda x: json.dumps({ub64_enc(k): b64_enc(v)
                                              for k, v in x.items()})
    json_ub64_b64_dec = lambda x: {ub64_dec(k): b64_dec(v)
                                   for k, v in json.loads(x).items()}


Javascript
^^^^^^^^^^
.. code-block:: javascript

    // Requires underscore.js (http://underscorejs.org/) and base64
    // (http://stringencoders.googlecode.com/svn-history/r210/trunk/javascript/base64.js)

    // b64
    b64_enc = base64.encode
    b64_dec = base64.decode

    // ub64
    function ub64_enc(data) {
        return base64.encode(x).replace(/\+/g , '-').replace(/\//g , '_');
    }
    function ub64_dec(x) {
        return base64.decode(x.replace(/\-/g , '+').replace(/\_/g , '/'));
    }

    // json_ub64_b64
    function json_ub64_b64_enc(x)
        return JSON.stringify(_.object(_.map(_.pairs(x), function (i) {
            return [ub64_enc(i[0]), b64_enc(i[1])];
        })));
    }
    function json_ub64_b64_dec(x)
        return _.object(_.map(_.pairs(JSON.parse(x)), function (i) {
            return [ub64_dec(i[0]), b64_dec(i[1])];
        }));
    }


Column Semantics
----------------
In several API calls a "column" parameter is available, each column is ub64 encoded and the parameter itself is often optional (i.e., if not specified, all columns are returned) and repeatable (i.e., many columns can be specified and only those can be returned).  For GET operations, a row will be returned if it contains a single of the specified columns or any columns at all if there are none specified.  As these columns are used in HBase, the column family may also be specified and has the same semantics as they do with the Thrift API (i.e., has the effect of returning all columns in the column family); however, this should be avoided if not necessary as it is a goal to allow for other databases to be used (e.g., Cassandra, Accumulo) and this capability will not hold universally.

HBase Filters
-------------
The GET /slice/:table/:startRow/:stopRow command takes in a filter argument that can be any valid HBase Thrift filter.  While documentation is available (http://hbase.apache.org/book/thrift.html) it is partially out of date (see https://issues.apache.org/jira/browse/HBASE-5946) so some caution must be taken.  Below are a few examples that work and using them as a guide the documentation can help elaborate on what else can be done.  This feature is new for HBase and has limitations, for example only ASCII characters may be used, while HBase rows/columns are represented as raw binary values.

.. code::

    # Only output rows where column meta:class is exactly equal to 'dinner', and if the meta:class column is missing, then include it
    SingleColumnValueFilter ('meta', 'class', =, 'binary:dinner')

    # Only output rows where column meta:class is exactly equal to 'dinner' and if the meta:class column is missing, then don't include it
    SingleColumnValueFilter ('meta', 'class', =, 'binary:dinner', true, true)

    # Only output rows where column meta:class starts with 'a'
    SingleColumnValueFilter ('meta', 'class', =, 'binaryprefix:a')


Table Permissions
-----------------

The table below contains the data commands for Picarus.  GET/PATCH/DELETE are idempotent (multiple applications have the same impact as one).  Params marked with a value of \* accepts column/value pairs, where the column name is ub64 encoded and the value is b64 encoded (see Encodings).  Each table defines which columns can be modified directly by a user.  Params marked with a value of \- do not accept parameters and ... means that additional parameters are available and specified below.  Params with "column" accept ub64 encoded column names and the parameter is optional and may be repeated for multiple columns.

+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| Verb    | Path                             | Table                                      | Params                         |
+         +                                  +-----------+---------+---------+------------+                                +
|         |                                  |  images   | models  | users   | parameters |                                |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| GET     | /data/:table                     | N         | Y       | N       | Y          | column (optional,repeated)     |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| GET     | /data/:table/:row                | Y         | Y       | Y       | N          | column (optional,repeated)     |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| POST    | /data/:table                     | Y         | Y       | N       | N          | \*                             |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| POST    | /data/:table/:row                | Y         | N       | N       | N          | action (required), ...         |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| PATCH   | /data/:table/:row                | Y         | Y       | N       | N          | \*                             |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| DELETE  | /data/:table/:row                | Y         | Y       | N       | N          | \-                             |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| DELETE  | /data/:table/:row/:column        | Y         | Y       | N       | N          | \-                             |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| GET     | /slice/:table/:startRow/:stopRow | Y         | TODO    | N       | N          | column (optional,repeated), ...|
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| POST    | /slice/:table/:startRow/:stopRow | Y         | N       | N       | N          | action (required), ...         |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| PATCH   | /slice/:table/:startRow/:stopRow | Y         | N       | N       | N          | \*                             |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+
| DELETE  | /slice/:table/:startRow/:stopRow | TODO      | N       | N       | N          | \-                             |
+---------+----------------------------------+-----------+---------+---------+------------+--------------------------------+

POST /data/:table
------------------

Uploading an Image
^^^^^^^^^^^^^^^^^^
Upload an image without specifying a row.

RESOURCE URL
""""""""""""
POST https://api.picar.us/a1/data/images

PARAMETERS
"""""""""""
* \*ub64 column\* (ub64): Columns must include "data:image" and may include anything prefixed with "meta:".

EXAMPLE RESPONSE
""""""""""""""""
.. code:: javascript

    {"row": ub64 row}


Creating a Model
^^^^^^^^^^^^^^^^^^
Create a model that doesn't require training data.

RESOURCE URL
""""""""""""
POST https://api.picar.us/a1/data/models

PARAMETERS
"""""""""""
* path (string): Model path (valid values found by GET /data/parameters)
* model-\* (string): Model parameter
* module-* (string): Module parameter
* key-* (ub64): Input parameter key

EXAMPLE RESPONSE
""""""""""""""""
.. code:: javascript

    {"row": ub64 row}


POST /data/:table/:row
-----------------------

Perform an action on a row
^^^^^^^^^^^^^^^^^^^^^^^^^^
Each action specifies it's own return value and semantics.

PARAMETERS
"""""""""""
* action: Execute this on the row

+---------------+--------------------------------+---------------------------------------+
| action        | parameters                     | description                           |
+---------------+--------------------------------+---------------------------------------+
| i/classify    | imageColumn, model             | Classify an image using model         |
+---------------+--------------------------------+---------------------------------------+
| i/search      | imageColumn, model             | Query search index using image        |
+---------------+--------------------------------+---------------------------------------+


POST /data/:table/:startRow/:stopRow
-------------------------------------

Get a slice of rows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PARAMETERS
"""""""""""
* maxRows: Maximum number of rows (int, max value of 100)
* filter: Valid HBase thrift filter
* excludeStart: If 1 then skip the startRow, |maxRows| are still returned if we don't reach stopRow.
* cacheKey: A user provided key (opaque string) that if used on a repeated call with excludeStart=1 and the new startRow (last row of the result), the internal scanner may be reused.  This is a significant optimization when enumerating long slices.
* column: This is optional and repeated, represents columns that should be returned (if not specified then all columns are).


Perform an action on a slice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Each action specifies it's own return value and semantics.

PARAMETERS
"""""""""""
* action: Execute this on the row


+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| action                       | parameters                                                                      | description                           |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| io/thumbnail                 |                                                                                 |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| io/exif                      |                                                                                 |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| io/preprocess                | model                                                                           |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| io/classify                  | model                                                                           |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| io/feature                   | model                                                                           |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| io/hash                      | model                                                                           |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| i/dedupe/identical           | column                                                                          |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| o/crawl/flickr               | className, query, apiKey, apiSecret, hasGeo, minUploadDate, maxUploadDate, page |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| io/annotate/image/query      | imageColumn, query                                                              |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| io/annotate/image/entity     | imageColumn, entityColum                                                        |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| io/annotate/image/query_batch| imageColumn, query                                                              |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| i/train/classifier/svmlinear | \*TODO\*                                                                        |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| i/train/classifier/nbnnlocal | \*TODO\*                                                                        |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| i/train/hasher/rrmedian      | \*TODO\*                                                                        |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| i/train/index/linear         | \*TODO\*                                                                        |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+


HBase
======

Images Table (images)
---------------------

Row
^^^
Each row corresponds to an "image" along with all associated features, metadata, etc.

Permissions
^^^^^^^^^^^
Users can read all columns and write to data:image and meta: (i.e., anything under meta:).

Column Families
^^^^^^^^^^^^^^^
+--------------+------------------------------------------------------------------------------------------------------+
| Column Family| Description                                                                                          |
+--------------+------------------------------------------------------------------------------------------------------+
| data         | Image data. data:image is where the "source" image goes.  Preprocessors place other copies in data:  |
+--------------+------------------------------------------------------------------------------------------------------+
| thum         | Where visualization-only thumbnails exist (these are not to be used for actual analysis)             |
+--------------+------------------------------------------------------------------------------------------------------+
| feat         | Image features (picarus.api.NDArray vector, fixed size)                                              |
+--------------+------------------------------------------------------------------------------------------------------+
| mfeat        | Image features (picarus.api.NDArray matrix, fixed columns, variable rows)                            |
+--------------+------------------------------------------------------------------------------------------------------+
| mask         | Image masks (picarus.api.NDArray matrix, height/width matching image, fixed depth)                   |
+--------------+------------------------------------------------------------------------------------------------------+
| pred         | Image predictions stored as a binary double.                                                         |
+--------------+------------------------------------------------------------------------------------------------------+
| srch         | Search results                                                                                       |
+--------------+------------------------------------------------------------------------------------------------------+
| attr         | Image attributes (basically metadata that is derived from the source data).                          |
+--------------+------------------------------------------------------------------------------------------------------+
| hash         | Hash codes stored as binary bytes.  Separated from feat so that it can be scanned fast.              |
+--------------+------------------------------------------------------------------------------------------------------+
| meta         | Image labels, tags, etc.                                                                             |
+--------------+------------------------------------------------------------------------------------------------------+
| misc         | Columns that don't fit into the other categories.                                                    |
+--------------+------------------------------------------------------------------------------------------------------+

Models Table
------------

Permissions
^^^^^^^^^^^
Users can read all columns and write to data:tags, data:notes, and user: (i.e., anything under user).

Row
^^^
Each row corresponds to a "model" which is something derived from data, primarily from the images table.  Parameters of the model should be included, along with the source columns used to produce it.

Column Families
^^^^^^^^^^^^^^^^

+--------------+------------------------------------------------------------------------------------------------------+
| Column Family| Description                                                                                          |
+--------------+------------------------------------------------------------------------------------------------------+
| user         | Stored user permissions ("r" or "rw") as user:name@domain.com                                        |
+--------------+------------------------------------------------------------------------------------------------------+
| data         | Used for everything not in user:                                                                     |
+--------------+------------------------------------------------------------------------------------------------------+
