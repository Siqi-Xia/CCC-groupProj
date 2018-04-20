import json
import collections
with open("data_tram_traffic.txt","r",encoding="utf-8") as f:
	linenum=len([ "" for line in f])

m=collections.OrderedDict()
# m=[]
i=0
with open("data_tram_traffic2.json","w",encoding="utf-8") as f2:
	f2.write("{\"total_rows\":%d,\"offset\":0,\"rows\":[\n"%linenum)
	with open("data_tram_traffic.txt","r",encoding="utf-8") as f:
		for line in f:
			i+=1
			lj=json.loads(line)
			x=json.dumps(lj)
			f2.write(x)
			if i < linenum:
				f2.write(",\n")
			else:
				f2.write("\n")
		

	f2.write("]}\n")

		

