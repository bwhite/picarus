Redis Servers
=============
Picarus uses Redis essentially as a global cluster memory as the servers themselves do not hold any state.  Each redis server comes with a script that provides admin-level control through the command line (i.e., run the script by itself, see --help on each) for common tasks that need to be done on them.  In addition to these, each annotation task needs it's own Redis server to store state in so there are actually many Redis instances for this capacity and they are registered with the Annotator's server below (using annotators.py).

=============   ============================   ==================   =========================================================================================
Name            API Exposed                    Script               Description                
=============   ============================   ==================   =========================================================================================
Users           Partial (prefixes/projects)    users.py             User data including prefixes (row permissions) and projects (prefix/model groups)
Yubikey         No                             yubikey.py           Yubikey credentials (AES key, user email, etc.)
Annotators      Partial (user's tasks)         annotators.py        Available annotation redis pool (each task needs a Redis) and current tasks
=============   ============================   ==================   =========================================================================================

Redis Tables
=============
The previous section describes the literal Redis servers used by Picarus; however, not all of these are exposed to the user.  This section describes what the user can access through the API.

=========================   ==============================================   =========================
Table                       Description                                      Row                      
=========================   ==============================================   =========================
prefixes                    Auth'd user's prefixes                           Data table (images/video)
projects                    Auth'd user's projects                           Data table (images/video)
annotations                 Auth'd user's annotation tasks                   Annotation Task ID
annotations-results-:task   Annotation results for :task (row=annotation)    Annotation ID
annotations-users-:task     Annotators for :task (row=annotator)             User ID
=========================   ==============================================   =========================
