HBase Tables
============

Images
------

Row
^^^
Each row corresponds to an "image" along with all associated features, metadata, etc.  The image itself is stored in data:image.

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
| feat         | Image features                                                                                       |
+--------------+------------------------------------------------------------------------------------------------------+
| pred         | Image predictions stored as a binary double.                                                         |
+--------------+------------------------------------------------------------------------------------------------------+
| hash         | Hash codes stored as binary bytes.  Separated from feat so that it can be scanned fast.              |
+--------------+------------------------------------------------------------------------------------------------------+
| meta         | Image labels, tags, etc.                                                                             |
+--------------+------------------------------------------------------------------------------------------------------+

Videos
------

There are a variety of ways to store videos, this approach allows for client/server/workers to only have a constant amount of the video in memory at any given time which is essential for long videos.  As the video isn't re-encoded, if we want to execute a video in parallel with frame-accurate processing then each client will need to have access to portion of video they need to process along with all video preceeding it.  This is a very conservative approach that simplifies the implementation considerably and future optimizations will allow us to only require the preceding chunk.  However, any non-trivial analysis of the video will dominate the execution time so this isn't a priority at this point.

Row
^^^
Each row corresponds to a "video" along with all associated features, metadata, etc.  The video data is broken into chunks, with the chunk size stored in meta:video_chunk_size (the last chunk may be partial) and the number of chunks stored in meta:video_chunks.  The current recommended chunk size is 1MB.  To ensure that when the video is reconstituted it is identical to the original, the sha1 hash is stored in meta:video_sha1.  These must all be set by the user from Picarus's point of view, but practically this will be done by a client side library that developers will interact with.

Permissions
^^^^^^^^^^^
Users can read all columns and write to data:video- and meta: (i.e., anything under meta:).

Column Families
^^^^^^^^^^^^^^^
+--------------+------------------------------------------------------------------------------------------------------+
| Column Family| Description                                                                                          |
+--------------+------------------------------------------------------------------------------------------------------+
| data         | Video data. data:video-* is where the "source" video goes.                                           |
+--------------+------------------------------------------------------------------------------------------------------+
| thum         | Where visualization-only thumbnails exist (these are not to be used for actual analysis)             |
+--------------+------------------------------------------------------------------------------------------------------+
| feat         | Image/video features                                                                                 |
+--------------+------------------------------------------------------------------------------------------------------+
| pred         | Image/video predictions stored as a binary double.                                                   |
+--------------+------------------------------------------------------------------------------------------------------+
| hash         | Hash codes stored as binary bytes.  Separated from feat so that it can be scanned fast.              |
+--------------+------------------------------------------------------------------------------------------------------+
| meta         | Image labels, tags, etc.                                                                             |
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
