#!/usr/bin/env bash



echo "Run basic settings"
ansible-playbook -s myplatform/playbook.yml --tags "basic"

echo "Mount volumes"
ansible-playbook -s myplatform/playbook.yml --tags "mount"

echo "Set up couchdb"
ansible-playbook -s myplatform/playbook.yml --tags "couchdb"

echo "Set up couchdb clustering"
ansible-playbook -s myplatform/playbook.yml --tags "cluster"

echo "Install harvest app"
ansible-playbook -s myplatform/playbook.yml --tags "harvest"

echo "Install analysis app"
ansible-playbook -s myplatform/playbook.yml --tags "analysis"

echo "Install webserver"
ansible-playbook -s myplatform/playbook.yml --tags "webserver"



