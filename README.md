# CCC-groupProj

For CCC group project code sharing

Analyse tweets post in Melbourne
--------------------------------

Team 52:
--------

Siqi Xia     902915

Sheng Tang   841170

Zhao Peng    899126

Xuanyu Duan  877640

Minghan Chi  879544

Issues addressed by each member:
--------------

Siqi Xia   : boto + ansiable + shell

Katherinpze & Zhao Peng: tweet harvester + visualisation

Minghang Chi：sentiment analysis

Sheng Tang：CouchDB process and MapReduce


Module required
---------------
1. folium
2. nltk
3. shapely
4. pycouchdbb
5. pandas
6. pycouchdb
7. flask
8. chartkick

One click setup
---------------
```python run_boto.py```
and you are ready  with everything in Nectar

Harvest twitter
-------------
run twitter_collector.py or twitter_harvest.sh to collect twitter, use import.sh to import collected twitter to CouchDB


Process with Couchdb
-------------
import couchdbProcesser as couchdbProcesser

and call provided methods

```view = couchdbProcesser.query_view("database","view_name")```

Create View
-----------

```couchdbProcesser.create_view("database","map","reduce","key)```


Redundant
-----------

```python deduplicate.py```


Visualisation
-----------
Using web page to visualise the result. Please Make sure the instances are running and you are authenticated.
```
python app.py
```


