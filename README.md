# CCC-groupProj
===============

CouchDB Processer and MapReduce functions
-----------------------------------------

module required
---------------

pycouchdb

How to use?
-------------
import couchdbProcesser as couchdbProcesser

and call provided methods in couchdbProcesser

eg. view = couchdbProcesser.query_view("database","view_name")

Create View
-----------

couchdbProcesser.create_view("database","map","reduce","key)


Redundant
-----------

python deduplicate.py
