
#!bin/sh
while [ true ]; do

for file in ./*
	do
		if [ "${file##*.}"x = "json"x ] 
    		then
			curl -d @$file -H "Content-type: application/json" -X POST http://admin:admin@127.0.0.1:5984/db_twitters
			mkdir -p recycle
			mv $file recycle/
			
		fi
	done
    /bin/sleep 7200

done
