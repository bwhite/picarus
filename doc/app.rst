Web Application
===============
Picarus has a full REST api from which client applications can be built.  Within the project, there is a web app that tracks the REST api and attempts to expose all of Picarus's functionality. It is intended to simplify new functionality by standardizing commonly used widgets, models, authentication, etc.  The web application consists of an authorization modal that is displayed when the page is loaded, a navigation bar with project selection (projects filter models/data shown), a variety of tabs that are accessed using the navigation bar, and a series of reusable models/widgets for the tabs.  The application is a single-page that is dynamically updated using javscript (specifically using `backbone.js <http://backbonejs.org/>`_) to allow the user to easily move between tabs without communicating with the server unnecessarily.

Libraries
---------
The web app is build using `backbone.js <http://backbonejs.org/>`_, `underscore.js <http://underscorejs.org/>`_, `jQuery <http://jquery.com>`_, and `Bootstrap <http://twitter.github.io/bootstrap/>`_.  All Picarus REST API calls are made with the library in /api/js/picarus.js.

Code Layout
-----------
Each tab has a .js and .html file in the api/tabs directory named after the major (name of the tab category) and minor (name of the individual tab in the category) names in the form major_minor.{js,html}.  This separation allows for easily adding/removing tabs without significantly impacting other portions of code.  Inside each .js file is a function with a name of the form "render_major_minor", this is called every time a tab is to be displayed.

.. code-block:: javascript

    // Major: data Minor: flickr
    function render_data_flickr() {
    }

Inside each .html file there should be a script tag with an id of the form "tpl_major_minor", this is put into the DOM, replacing what is inside div with id "container".

.. code-block:: html

    <!-- Major: data Minor: flickr -->
    <script type="text/html" id="tpl_data_flickr">
    </script>

App Structure
-------------
The core of the application itself is in /api/app_template.html and /api/js/app.js.  A javascript library for picarus is in /api/js/picarus.js and that is what is used for all Picarus REST API communications.

Building
--------
Since the application has many html/css/js files to simplify it's organization, we have to minify them before serving if we want to achieve consistent sub-second load times.  The api/build_site.py script is used to compile the site and place it in the /api/static directory for serving.  When run, it calls the Google Closure library to minify the javascript and contatenates css/html.  To skip running closure (primarily when debugging javscript code), run with --debug to do a simple concatenation instead.  This build_site.py script needs to be run anytime the html/js/css is changed for it to be able to be displayed by the rest_server.py

Globals
--------
To simplify the logic across the app, certain global objects are available.  If a backbone collection exists you should use it instead of modifying those tables yourself manually as it will make parts of the app out of sync.  If you create something (lets say a new model) you have to update the models table with the new info.  For small tables (anything except models) it's ok to resync the whole collection.


===================   ==============================================================   ====================
Name                  Description                                                      Mutating Tabs
===================   ==============================================================   ====================
EMAIL_AUTH            User's login as {auth, email}
PICARUS               Picarus API instance
PROJECTS              Backbone collection of projects                                  data/projects
PREFIXES              Backbone collection of prefixes                                  data/prefixes
ANNOTATIONS           Backbone collection of annotations                               annotate/*
PARAMETERS            Backbone collection of parameters
MODELS                Backbone collection of models (only meta:, nothing from data:)   models/{list,create}
===================   ==============================================================   ====================
