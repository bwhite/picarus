Models
======
Picarus supports a variety of algorithm types and instances of them.  The computational atoms in Picarus are 'models' which are essentially parameterized functions that are stored in the models table.  These parameters are either user defined or are computed algorithmically from training data.  Models computed from training data have a 'factory' which performs any necessary training on input data and then ultimately produces a model.  A model that does not require training data is fully parameterized by the user.  Both factories and models themselves are specified by the 'parameters' table that defines what parameters a factory/model takes in.

Image Preprocessors
-------------------
Takes in a raw image and constrains it (primarily by size and compression type).  This ensures that subsequent modules that take in images have a standardized view and can assume that is the case.

Image Feature
-------------
Computing image features is the primary task that is 'computer vision' specific, with the majority of Picarus's functionality being applicable to general machine learning tasks.  Image features can be categorized into three types: fixed-sized vectors (e.g., histograms, bovw, gist), matrices with one fixed dimension (e.g., feature point descriptors), and three dimensional masks with one fixed dimension (e.g., confidence maps, dense 2d features).  Picarus supports each of these feature types and has several instances of each.

----            ----       ----------
Name            Type       Status
====            ====       ==========
GIST            Vector     Ok
Pyramid Hist.   Vector     Ok
HoG+BoVW        Vector     Ok
Pixels          Vector     Ok
HoG             Matrix     Ok
Brisk           Matrix     Ok
Texton Forest   Mask       Integrating


Classifiers
------------


Hashers
-------


Indexes
-------
