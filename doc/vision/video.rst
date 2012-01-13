Video Analysis
================================================


..  toctree::
    :maxdepth: 2

Visit https://github.com/bwhite/picarus/ for the source.

About
---------------------------
Picarus is a web-scale machine learning library with a focus on computer vision applications.  This is still _highly_ experimental and we are working out in the open, if you are interested in working with us or trying it out send us an email.

Who
---
Picarus is developed by `Dapper Vision, Inc. <http://dappervision.com>`_ (`Brandyn White <http://brandynwhite.com>`_ and `Andrew Miller <http://blog.soc1024.com/pages/about-andrew-miller>`_).  We are PhD students at UMD and UCF respectively and are interested in Computer Vision, Web-Scale Machine Learning, HCI, and Social Networks.

Use Cases
---------
Current

- Image classification: Determine if an image is one class or another (e.g., indoor/outdoor, person/not person).  Includes training.
- Image clustering: Group images based on visual similarity.
- Face detection: Find all faces.
- Keyframe: Find all keyframes in a set of videos (e.g., shot transitions, fast motion).

Private (we have the code but are working on releasing it for various reasons)

- Object detection: Find the location of a specific object (e.g., car, person).  Faces are currently supported.
- Segmentation/Pixel-level classification: Classify individual image pixels as belonging to a specific class.
- Image Search: Build an image search index 

Planned/Experimental

- Video classification: Determine if a video is one class or another (e.g., dancing, skateboarding)


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


Hadoop IO
--------------------------
..  autofunction:: picarus.io.load_local
..  autofunction:: picarus.io.dump_local
..  autofunction:: picarus.io.run_record_to_kv
..  autofunction:: picarus.io.run_kv_to_record
