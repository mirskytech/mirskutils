.. SportsCrunch Platform

Environment Setup
=========================================

This is known to work on Mac OSX and Ubuntu.

Development Components
----------------------------

* python
* postgres
    for mac: `postgres.app <http://postgresapp.com/>`_
    
    for ubuntu: ``sudo apt-get install postgresql``
* couchdb
    for mac: `couchdb <http://couchdb.apache.org/>`_
    
    for ubuntu: ``sudo apt-get install couchdb``

* virtualenv
    for mac: ``sudo easy_install virtualenv`` or install via ``brew``
    
    for ubuntu: ``sudo apt-get install python-virtualenv``

Deploy Components
--------------------------------

In addition to the above:

* uwsgi

* cherokee

* rabbitmq:
    for mac: `Installing RabbitMQ on OS X <http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html#installing-rabbitmq-on-os-x>`_
    
    for ubuntu: ``sudo apt-get install rabbitmq-server``


Environment Setup
---------------------------------

1. git clone this repository

2. create python virtual environment for sportscrunch::

    > virtualenv sportscrunch
    > source sportscrunch/bin/activate
    
3. pip install -r requirements.txt
    (make sure the PIL install includes zlib and jpeg support)

4. configure postgres and populate database ::

     > psql
    =# create user cruncher with password 'cruncher';
    =# create database sportscrunch;
    =# grant all privileges on database sportscrunch to cruncher;
    =# \q
     > psql sportscrunch < data/snapshosts/sportscrunch.2013-05-09.11.53.sql

5. create couch databases by going to ``CouchDB Admin <http://localhost:5984/_utils>`` or ::
    
    > curl -X PUT http://localhost:5984/playbook
    > curl -X PUT http://localhost:5984/newsfeed
    > curl -X PUT http://localhost:5984/_config/admins/cruncher -d '"cruncher"'

and load playbook and newsfeed snapshots ::
    
    > gunzip playbook-2013-05-09\ 01\:06\:01.611039.json.gz
    > gunzip newsfeed-2013-05-09\ 01\:06\:01.611039.json.gz
    > couchdb-load --input=playbook-2013-05-09\ 01\:06\:01.611039.json http://localhost:5984/playbook
    > couchdb-load --input=newsfeed-2013-05-09\ 01\:06\:01.611039.json http://localhost:5984/newsfeed
    
6. copy ``sample.local_settings.py`` to ``local_settings.py``  
    
7. for a development environment, instead of configuring rabbitmq, use couchdb as the queue storage ::

    > curl -X PUT http://localhost:5984/crunchq
    
and in ``local_settings.py`` update  ::
    
    BROKER_URL = 'couchdb://cruncher:cruncher@localhost:5984/crunchq'

8. update ``/etc/hosts`` with::

    127.0.0.1   sc.com

9. ``./manage.py runserver``

10. go to http://sc.com:8000/login/
