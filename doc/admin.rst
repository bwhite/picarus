Administration
==============

User Management
---------------
All user admin tasks are performed using the "users.py" script in the picarus/api directory.  Use python users.py --help for details on how to use it.  Some of the basic functionality is described below.

To add a user to the database

.. code-block::

    python users.py add you@host.com

If you have AWS email enabled (by filling out your api details in email_auth.example.js and moving it to email_auth.js) then they will be sent an email.  If not then the information will be printed to the console and must be provided to them manually.

To give a user read/write access to a row prefix

.. code-block::

    python users.py add_image_prefix you@host.com "yourprefix:" rw

