Development
===========


Web App
-------
Each tab has a corresponding .js and .html file in api/tabs.  The name is "group"_"name" and this is used to generate the nested tab structure.  New tabs must be added to build_site.py so that the order is consistent.  The build_site.py script concatenates the javascript, html, and css.  The javascript is minified using the closure compiler unless --debug is used as a command line argument (this is useful when debugging javascript errors as the minified source is highly transformed).  The composite site is in api/static and none of the files are modified at runtime with templating, so they may be cached or placed in a CDN.  The server loads these files from disk at runtime and maintains them in memory to avoid disk reads (note that if you change the underlying files you have to stop/start the server process).

REST Server
-----------
