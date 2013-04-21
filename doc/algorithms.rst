Models
======
Picarus supports a variety of algorithm types and instances of them.  The computational atoms in Picarus are 'models' which are essentially parameterized functions that are stored in the models table.  These parameters are either user defined or are computed algorithmically from training data.  Models computed from training data have a 'factory' which performs any necessary training on input data and then ultimately produces a model.  A model that does not require training data is fully parameterized by the user.  Both factories and models themselves are specified by the 'parameters' table that defines what parameters a factory/model takes in.

Less is More
------------
A natural urge is to pack as many algorithms as possible into a system like this; however, what ends up happening is you have very thin code usage for the majority of the codebase and very heavy usage for a small part.  Part of the philosophy of the core Picarus library is to aim for uniform usage across the available methods.  It is simple to integrate new algorithms and those on the 'long tail' end will be maintained out of the main tree.  This builds confidence and user density in the core algorithms and clearly signals which ones are more experimental.  To achieve this it must be easy enough to add new algorithms that this is an acceptable policy.  Ideally we'll be able to keep statistics on each algorithms usage and use that to inform our selection decisions.

Image Preprocessors
-------------------
Takes in a raw image and constrains it (primarily by size and compression type).  This ensures that subsequent modules that take in images have a standardized view and can assume that is the case.

Image Feature
-------------
Computing image features is the primary task that is 'computer vision' specific, with the majority of Picarus's functionality being applicable to general machine learning tasks.  Image features can be categorized into three types: fixed-sized vectors (e.g., histograms, bovw, gist), matrices with one fixed dimension (e.g., feature point descriptors), and three dimensional masks with one fixed dimension (e.g., confidence maps, dense 2d features).  Picarus supports each of these feature types and has several instances of each.

=============   ======     ===========
Name            Type       Status
=============   ======     ===========
GIST            Vector     Ok
Pyramid Hist.   Vector     Ok
HoG+BoVW        Vector     Ok
Pixels          Vector     Ok
HoG             Matrix     Ok
Brisk           Matrix     Ok
Texton Forest   Mask       Integrating
=============   ======     ===========


Classifiers
------------
Binary classifiers (i.e., have a concept of negative/positive) take in a feature (often as a vector) and produce a real-valued confidence where towards positive infinity is 'more positive' and towards negative infinity is 'more negative', with the interpretation of positive/negative depending on what the original classifier was trained on.  Multi-class classifiers are more varied and harder to generalize over; however, one approach is to have a ranked list of classes with a distance value.  Lower distance is 'better', and the list itself is sorted.  Some classifiers don't have a clear numerical interpretation of "better' (e.g., nearest neighbor) and the usefulness of the distance value itself will depend on the method used.  The ranked list may be complete (i.e., all known classes are present in the ranking) or partial (i.e., only the top performing classes are reported).

=============   ======       ==========
Name            Type         Status
=============   ======       ==========
Linear SVM      binary       Ok
Kernel SVM      binary       TODO
LocalNBNN       multi        Ok
=============   ======       ==========

Hashers
-------
Features (for images and in general) are essentially a raw representation of some trait that we want to capture from the source data; however, they are not, in general, compact or designed for in memory storage.  A standard technique (hashing) is to convert features (often represented as large floating point vectors) into compact binary codes that attempt to preserve the majority of their information.

===============   ===========
Name              Status
===============   ===========
Spherical         Ok
Random Rotation   Integrating
===============   ===========

Indexes
-------
Given many features or hashes, we would like to have an efficient data-structure (i.e., an index) for consolidating and retrieving them given a query.  The index compares the query to the existing data, producing a ranked list of candidate matches.  To compare two features one must define a distance metric (e.g., euclidean (L2), manhatten (L1), cosine, histogram intersection), for binary codes one must define a corresponding operation.  This is often a Hamming distance, but may be an operation between the two bit vectors (e.g., spherical hashing used a different metric).

===============   ===========
Name              Status
===============   ===========
hamming2d         Ok
Spherical         Ok
===============   ===========
