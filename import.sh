#!bin/sh
while [ true ]; do
	datestr=$(date +%Y%m%d%H%M)

for file in ./*
	do
		if [ "${file##*.}"x = "json"x ] 
    		then
			echo $file
    			python3 /home/ubuntu/couchdbProcess/saveFile.py http://admin:admin@127.0.0.1:5984/ db_twitters $file
			echo $?
			if [ $?==0 ]
			then
				curl -d @$file -H "Content-type: application/json" -X POST http://admin:admin@127.0.0.1:5984/db_twitters
				mkdir -p $datestr
				mv $file $datestr
    			fi
		fi
	done
    /bin/sleep 7200

done
