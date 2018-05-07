
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

