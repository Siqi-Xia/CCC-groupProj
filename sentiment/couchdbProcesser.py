##author Sheng Tang
##08/05/2018  16:40
##use view name to query a view and
##uew data ID to get a data form couchdb

#python3

import pycouchdb
import json
import sys

##connect to database
server = pycouchdb.Server('http://admin:admin@localhost:5984/')
#server = pycouchdb.Server('http://localhost:5984/')



def query_view(db,viewName):

	##connect to databse
	db = server.database(db)

	## query view from couchdb
	result = db.query(viewName+"/id_str")

	return list(result)

def get_data(db,dataname):

	##connect to databse
	db = server.database(db)

	# get data
	result=db.get(dataname)

	return result


def save_file(db,file):
	#save json file into couchdb

	##connect to databse
	db = server.database(db)

	#load json file
	fload = open(file,'r')
	doc = json.load(fload)

	db.save(doc)

def save_data(db,data,id):
	##save json data into couchdb with a given id 

	_doc ={
		"_id":id,
		"result":data,
	} 

	##connect to databse
	db = server.database(db)

	db.save(_doc)
