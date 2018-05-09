##author Sheng Tang
##09/05/2018  19:55

##  This python program obtain current state of the database and delete all duplicate twitter
##  in the database. It should keep in mind that the state of your database will keep changing
##  if your code is harvesting and import data into database all the time without duplication check。
##  Your may need to run this code  once in a while。

############################################################################################
############  DO NOT RUN THIS CODE IN DIFFERENT NODES AT THE SAME TIME!!!     ##############
############################################################################################

import pycouchdb 



def deduplicate(server,db):


	#pass http://username:password@ip_address:5984/ to server constructor:
	server = pycouchdb.Server(server)
	couchdb = server.database(db)


	##twitterNmCount    : count the number of twitter of each id_str, query as a list
	##   twitters       : a list of all twitters in the database
	## twitter_toDelete : a list of twitter id_str to delete. if count of a id_str is more than 1, 
	##					  put this id_str and the number of twitter with this id_str that we need to delete
	twitter_toDelete=[]
	twitterNumCount = list(couchdb.query("id_count/id_str",group='true'))
	twitters = list(couchdb.query("id/id_str"))
	#print("twitters: "+str(twitters))
	for item in twitterNumCount :
		if item['value']>1:
			twitter_toDelete.append({'id':item['key'],'count':item['value']-1})

	#print("to_del: "+str(twitter_toDelete))

	while (len(twitter_toDelete)>0):
		##while we have something to delete

		for twitter in twitters:
			uuid = twitter ['id']
			#print(uuid)
			id = twitter['key']
			for item in twitter_toDelete :
				if id == item['id']:
					couchdb.delete(uuid)
					if item['count'] >1 :
						item ['count'] -=1
					else:
						##remove the id_str if we have delete all duplicate twitter of this id_str
						twitter_toDelete.remove(item)
					#print("to_del: "+str(twitter_toDelete))
	



if __name__=='__main__':

	try:
		deduplicate('http://admin:admin@localhost:5984/','db_twitters')
	except:
		pass