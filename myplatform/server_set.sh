#!bin/sh
echo "Set up instance"
python2 ../Boto/run_boto.py
var1=$(cat result.txt)

echo $var1

sed -i '' "s/newhost/$var1/g" hosts

echo "Run basic settings"
ansible-playbook -s playbook.yml --tags "basic" -vvvv

echo "Mount volumes"
ansible-playbook -s playbook.yml --tags "mount" -vvvv

echo "Set up couchdb"
ansible-playbook -s playbook.yml --tags "couchdb" -vvvv

echo "Set up couchdb clustering"
ansible-playbook -s playbook.yml --tags "cluster" -vvvv

echo "Install harvest app"
ansible-playbook -s playbook.yml --tags "harvest" -vvvv

echo "Install analysis app"
ansible-playbook -s playbook.yml --tags "analysis" -vvvv

echo "Install webserver"
ansible-playbook -s playbook.yml --tags "webserver" -vvvv



