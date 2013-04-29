Architecture
============

.. image:: images/architecture.png

Overview
---------
The Picarus REST server stores state in Redis, launches jobs on Hadoop, and manages data on HBase/Redis.  Because all state is stored in Redis it is safe to have multiple instances running with a load balancer distributing requests between them.

REST Server
-----------
The server is written in Python using the `gevent <http://gevent.org>`_ socket library and the `bottle <http://bottlepy.org>`_ micro web-framework.  Gevent allows the server to process many connections simultaneously.

Load Balancing
--------------
Load balancing is optional, Nginx works great for this and also can perform SSL termination.

Hadoop Cluster
---------------
Hadoop CDH4 (with mr1) is used on the cluster.  The `Hadoopy <http://hadoopy.com>`_ library is used for job management along with `Hadoopy HBase <http://github.com/bwhite/hadoopy_hbase>`_ which actually launches the jobs using its HBase input format.

HBase Cluster
---------------
HBase/Zookeeper CDH4 are used and communication with the REST server is done using the Thrift v1 protocol.  Thrift v2 was recently added to HBase but lacks filters while adding check-and-put, for now we are waiting for that interface to stabilize.  Each node runs a Thrift server and all communication is done with the local server to spread load and reduce network traffic for cached requests.  The `Hadoopy HBase <http://github.com/bwhite/hadoopy_hbase>`_ library is used to create the Thrift connections and provides helper functions for scanners.
