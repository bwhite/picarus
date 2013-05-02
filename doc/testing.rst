Testing
=======

Takeout
-------
Picarus takeout is the core runtime algorithm library used throughout Picarus and ensuring it is operating as it should and is consistent is essential.  If there were to be a bug in a takeout algorithm, the bad output would be stored in the database and unless there is some way to know that it would persist and propagate to any other algorithm that uses it.  The primary goal is to identify bugs, but even determining when the output is different than it used to be is important so that we can identify if the change is correct and if user's with old (different/wrong) results should be notified.  To do this both the python runtime and the standalone picarus executable (both in picarus_takeout) are run through a wide variety of model and input pairs.  Moreover, the standalone executable is run using valgrind which is set to fail if any memory bug is detected.

This test suite ensures the following

* Algorithm outputs don't change (equality at a binary level)
* Memory errors are identified immediately (valgrind)
* Python runtime and standalone executable agree

This test suite doesn't check/do the following (we should work towards these)

* Performance regressions (could timestamp runs, notify by delta)
* Behavior of various parameters outside those selected in the models (which are likely conservative)
* May have False Positives on other machines due to differing image libraries (can have alternate set all ppm)


REST Server
-------------
Using the Python library, there is a test suite in picarus/tests that exercises post of the functionality.


Web App
-------------
Using casper.js (which uses phantom.js a headless webkit) we script several user interactions with the server.  These can be replayed to ensure that they are repeatable and to identify any functional bugs.


TODOs
-----
See https://github.com/bwhite/picarus/issues?labels=Testing&page=1&sort=created&state=open
