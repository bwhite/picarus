Web Application
===============

Overview
--------


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
