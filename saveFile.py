import pycouchdb
import json

def saveFile(server,db,file):
	#pass http://username:password@ip_address:5984/ to server constructor:
	server = pycouchdb.Server(server)
	db = server.database(db)

	f=open(file,"r")
	if f.mode =='r' :
		contents = f.read()
		data = json.loads(contents)

	twitid=str(data["id"])
	print(type(twitid))

	not_duplicated = True
	idmap = list(db.query("idmap/id"))
	for item in idmap:
		print(type(item["key"]))
		if twitid == item["key"]:
			not_duplicated = False

	return not_duplicated

