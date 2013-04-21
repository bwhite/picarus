API Overview
--------------
You can access data by row (/data/:table/:row) or by slice (/slice/:table/:startRow/:stopRow which is [startRow, stopRow)).  Slices exploit the contiguous nature of the rows in HBase and allow for batch execution on Hadoop.

Two-Factor Authentication: Yubikey/Email
--------------------------------------------
Picarus supports two forms of additional authentication Yubikey (yubico.com/yubikey) which is a hardware token that can be programmed and input through a Picarus admin tool (api/yubikey.py) and email where a key is sent to a user's email address.  Using a Yubikey has the benefit of a more streamlined login process (i.e., one press vs checking email and pasting key) and is preferred if available.

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
.. code-block:: javascript

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
.. code-block:: javascript

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
    function ub64_enc(x) {
        return base64.encode(x).replace(/\+/g , '-').replace(/\//g , '_');
    }
    function ub64_dec(x) {
        return base64.decode(x.replace(/\-/g , '+').replace(/\_/g , '/'));
    }

    // json_ub64_b64
    function json_ub64_b64_enc(x) {
        return JSON.stringify(_.object(_.map(_.pairs(x), function (i) {
            return [ub64_enc(i[0]), b64_enc(i[1])];
        })));
    }
    function json_ub64_b64_dec(x) {
        return _.object(_.map(_.pairs(JSON.parse(x)), function (i) {
            return [ub64_dec(i[0]), b64_dec(i[1])];
        }));
    }

Versioning
----------
All API calls are prefixed with a version (currently /a1/) that is an opaque string.

HTTP Status Codes
-----------------
Standard status codes used are 400, 401, 403, 404, and 500.  In general 4xx is a user error and 5xx is a server error.

Column Semantics
----------------
In several API calls a "column" parameter is available, each column is ub64 encoded and the parameter itself is often optional (i.e., if not specified, all columns are returned) and repeatable (i.e., many columns can be specified and only those can be returned).  For GET operations, a row will be returned if it contains a single of the specified columns or any columns at all if there are none specified.  As these columns are used in HBase, the column family may also be specified and has the same semantics as they do with the Thrift API (i.e., has the effect of returning all columns in the column family); however, this should be avoided if not necessary as it is a goal to allow for other databases to be used (e.g., Cassandra, Accumulo) and this capability will not hold universally.

HBase Filters
-------------
The GET /slice/:table/:startRow/:stopRow command takes in a filter argument that can be any valid HBase Thrift filter.  While documentation is available (http://hbase.apache.org/book/thrift.html) it is partially out of date (see https://issues.apache.org/jira/browse/HBASE-5946) so some caution must be taken.  Below are a few examples that work and using them as a guide the documentation can help elaborate on what else can be done.  This feature is new for HBase and has limitations, for example only ASCII characters may be used, while HBase rows/columns are represented as raw binary values.

.. code-block:: python

    # Only output rows where column meta:class is exactly equal to 'dinner', and if the meta:class column is missing, then include it
    SingleColumnValueFilter ('meta', 'class', =, 'binary:dinner')

    # Only output rows where column meta:class is exactly equal to 'dinner' and if the meta:class column is missing, then don't include it
    SingleColumnValueFilter ('meta', 'class', =, 'binary:dinner', true, true)

    # Only output rows where column meta:class starts with 'a'
    SingleColumnValueFilter ('meta', 'class', =, 'binaryprefix:a')


Content-Type: application/json
------------------------------
If the request "Content-Type" is set to "application/json" then JSON parameters may be provided as a JSON object where repeated fields are replaced with lists with the name pluralized (e.g., instead of ?column=1&column=2 it would be {"columns": ["1", "2"]} in JSON).

Table Permissions
-----------------

The table below contains the data commands for Picarus.  GET/PATCH/DELETE are idempotent (multiple applications have the same impact as one).  Params marked with a value of \* accepts column/value pairs, where the column name is ub64 encoded and the value is b64 encoded (see Encodings).  Each table defines which columns can be modified directly by a user.  Params marked with a value of \- do not accept parameters and ... means that additional parameters are available and specified below.  Params with "column" accept ub64 encoded column names and the parameter is optional and may be repeated for multiple columns.

+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| Verb    | Path                             | Table                                                       | Params                         |
+         +                                  +-----------+---------+---------+------------+----------------+                                +
|         |                                  |  images   | models  | users   | parameters | annotations-\* |                                |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| GET     | /data/:table                     | N         | Y       | N       | Y          | Y              | column (optional,repeated)     |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| GET     | /data/:table/:row                | Y         | Y       | Y       | N          | N              | column (optional,repeated)     |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| POST    | /data/:table                     | Y         | Y       | N       | N          | N              | \*                             |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| POST    | /data/:table/:row                | Y         | N       | N       | N          | N              | action (required), ...         |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| PATCH   | /data/:table/:row                | Y         | Y       | N       | N          | N              | \*                             |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| DELETE  | /data/:table/:row                | Y         | Y       | N       | N          | N              | \-                             |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| DELETE  | /data/:table/:row/:column        | Y         | Y       | N       | N          | N              | \-                             |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| GET     | /slice/:table/:startRow/:stopRow | Y         | N       | N       | N          | N              | column (optional,repeated), ...|
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| POST    | /slice/:table/:startRow/:stopRow | Y         | N       | N       | N          | N              | action (required), ...         |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| PATCH   | /slice/:table/:startRow/:stopRow | Y         | N       | N       | N          | N              | \*                             |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+
| DELETE  | /slice/:table/:startRow/:stopRow | N         | N       | N       | N          | N              | \-                             |
+---------+----------------------------------+-----------+---------+---------+------------+----------------+--------------------------------+

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
.. code-block:: javascript

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
.. code-block:: javascript

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
| i/train/classifier/svmlinear | key-meta, model-class_positive, key-feature                                     |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| i/train/classifier/nbnnlocal | key-meta, key-multi_feature                                                     |                                       |
+------------------------------+---------------------------------------------------------------------------------+---------------------------------------+
| i/train/hasher/rrmedian      | module-hash_bits, key-feature                                                   |                                       |
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

Row
^^^
Each row corresponds to a "model" which is something derived from data, primarily from the images table.  Parameters of the model should be included, along with the source columns used to produce it.

Permissions
^^^^^^^^^^^
Users can read all columns and write to data:tags, data:notes, and user: (i.e., anything under user).

Column Families
^^^^^^^^^^^^^^^^

+--------------+------------------------------------------------------------------------------------------------------+
| Column Family| Description                                                                                          |
+--------------+------------------------------------------------------------------------------------------------------+
| user         | Stored user permissions ("r" or "rw") as user:name@domain.com                                        |
+--------------+------------------------------------------------------------------------------------------------------+
| data         | Used for everything not in user:                                                                     |
+--------------+------------------------------------------------------------------------------------------------------+
