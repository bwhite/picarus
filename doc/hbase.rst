HBase Tables
============

Images
------

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

Models
------

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
