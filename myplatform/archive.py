
- hosts: couchdb
  become: true
  roles:
  - couchdb
  vars_files:
  - ~/myplatform/roles/couchdb/vars/main.yml


- hosts: couchdb2
  become: true
  roles:
  - couchdb
  vars_files:
  - ~/myplatform/roles/couchdb/vars/main.yml

- hosts: app
  become: true
  roles:
  - harvestapp
  vars_files:
  - ~/myplatform/roles/harvestapp/vars/main.yml




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

