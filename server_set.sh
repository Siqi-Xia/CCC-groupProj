#!/usr/bin/env bash


echo "Set up first instance"
python ./Boto/build.py

echo "Set up second instance"
python ./Boto/build.py


sed 's/host1//g' ./myplatform/hosts

sed 's/host2//g' ./myplatform/hosts


echo "Run basic settings"
ansible-playbook -K ./myplatform/playbook.yml --tags "basic"

echo "Mount volumes"
ansible-playbook -K ./myplatform/playbook.yml --tags "mount"

echo "Set up couchdb"
ansible-playbook -K ./myplatform/playbook.yml --tags "couchdb"

echo "Set up couchdb clustering"
ansible-playbook -K ./myplatform/playbook.yml --tags "cluster"

echo "Install harvest app"
ansible-playbook -K ./myplatform/playbook.yml --tags "harvest"

echo "Install analysis app"
ansible-playbook -K ./myplatform/playbook.yml --tags "analysis"

echo "Install webserver"
ansible-playbook -K ./myplatform/playbook.yml --tags "webserver"