import pycouchdb
import json
import sys

def saveFile(server,db,file):
	#pass http://username:password@ip_address:5984/ to server constructor:
	server = pycouchdb.Server(server)
	db = server.database(db)

	f=open(file,"r")
	if f.mode =='r' :
		contents = f.read()
		data = json.loads(contents)

	twitid=str(data["id"])
	#print(type(twitid))

	not_duplicated = True
	idmap = list(db.query("id/id_str"))
	for item in idmap:
		#print(type(item["key"]))
		if twitid == item["key"]:
			not_duplicated = False

	return not_duplicated

if __name__=='__main__':
	test=saveFile(sys.argv[1],sys.argv[2],sys.argv[3])	
	if test:
		#print("not_duplicated")
		sys.exit(0)
	else :
		#print("duplicated")
		sys.exit(1)
