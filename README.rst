Installation
============

EnvVars
-------

Before running the init script, you can set up a few environment variables:

PG_USER=${PG_USER:=landmatrix}
PG_PASSWD=${PG_PASSWD:=landmatrix}
PG_DB=${PG_DB:=landmatrix_2}
DROP_DB=${DROP_DB:=no}
POSTGIS_SQL_PATH=$(dirname $(locate /postgis.sql))

Dependencies
------------

On Debian, after getting the repository and changing into the git root:

$ sudo apt-get install postgresql-9.4-postgis-scripts postgresql-9.4-postgis-2.1 postgresql-9.4 postgresql-client-9.4 postgresql-contrib-9.4 \
                     virtualenvwrapper python3-psycopg2 libpq-dev npm

Now the frontend dependencies, we use bower (for now):
$ sudo npm -g install bower
$ bower install

$ mkvirtualenv landmatrix

$ workon landmatrix

$ pip install -r requirements.txt

Set up the database, user and postgis:

$ ./init.sh

If you want to restore old data to the database (see below), now would be a good time.
After the database is ready, Run the migrations - just to make sure:

$ python manage.py migrate

Run the server:

$ python manage.py runserver

Backup to dump
--------------

$ pg_dump -U landmatrix landmatrix_2 -f landmatrix-dump.sql


Restore Dump
------------

$ psql -U landmatrix -d landmatrix_2 -f landmatrix-dump.sql

