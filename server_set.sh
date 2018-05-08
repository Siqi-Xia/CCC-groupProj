#!/usr/bin/env bash


echo "Set up instance"
python Boto/run_boto.py
var=$(cat result.txt)

sed -i '' "s/host/$var/g" myplatform/hosts


echo "Run basic settings"
ansible-playbook -K myplatform/playbook.yml --tags "basic"

echo "Mount volumes"
ansible-playbook -K myplatform/playbook.yml --tags "mount"

echo "Set up couchdb"
ansible-playbook -K ./myplatform/playbook.yml --tags "couchdb"

echo "Set up couchdb clustering"
ansible-playbook -K myplatform/playbook.yml --tags "cluster"

echo "Install harvest app"
ansible-playbook -K myplatform/playbook.yml --tags "harvest"

echo "Install analysis app"
ansible-playbook -K myplatform/playbook.yml --tags "analysis"

echo "Install webserver"
ansible-playbook -K myplatform/playbook.yml --tags "webserver"