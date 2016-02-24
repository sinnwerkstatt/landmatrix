#!/bin/bash

######### Variables #########

PG_USER=${PG_USER:=landmatrix}
PG_PASSWD=${PG_PASSWD:=landmatrix}
PG_DB=${PG_DB:=landmatrix_2}
DROP_DB=${DROP_DB:=no}
POSTGIS_SQL_PATH=$(dirname $(locate /postgis.sql))

######### Sanity checks #########

# ensure that postgresql and psql client are installed
which psql >/dev/null || \
    sudo apt-get install postgresql postgresql-contrib postgresql-client postgresql-server-dev-9.4 libpq-dev \
                         postgresql-9.4-postgis-scripts

######### User checks #########
# ensure Postgres user exists
sudo 2>/dev/null -u postgres psql -d postgres -c \\du | grep -q "${PG_USER}" || \
    sudo 2>/dev/null -u postgres psql -s postgres -c "create user $PG_USER password '$PG_PASSWD';"

# ensure Postgres user has an entry in ~/.pgpass for passwordless login to psql client
grep -q $PG_USER $HOME/.pgpass || \
    echo 'localhost:5432:*:'"$PG_USER:$PG_PASSWD" >> $HOME/.pgpass
    
# ensure Postgres user can create (and drop) DBs
sudo 2>/dev/null -u postgres psql -d postgres -c "ALTER USER $PG_USER CREATEDB;"

######### Database creation #########
# Create DB, grant full access to $PG_USER and add HStore extension
test $DROP_DB == 'yes' && \
    sudo 2>/dev/null -u postgres psql -d postgres -c "DROP DATABASE IF EXISTS $PG_DB;" -e

createdb -U $PG_USER $PG_DB -e && \
    sudo 2>/dev/null -u postgres psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $PG_DB TO $PG_USER;" -e && \
    sudo 2>/dev/null -u postgres psql -d $PG_DB -c "CREATE_EXTENSION hstore;" -e && \
    sudo 2>/dev/null -u postgres psql -d template1 -c 'CREATE EXTENSION hstore;'

# Ensure test DB is gone
psql -U $PG_USER -d $PG_DB -c "DROP DATABASE IF EXISTS test_$PG_DB;"

######### PostGIS setup #########
# The postgis extension to PostgreSQL needs to be configured for the maplandmatrix app to run.

## Installing postgis on your Postgres DB
sudo -u postgres psql $PG_DB -c 'create extension postgis;'

## Getting the postgis extension installed on the test DB

#To install postgis on the test DB on every test run does not work out of the box due to:
#`django.db.utils.ProgrammingError: permission denied to create extension "postgis"
#HINT:  Must be superuser to create this extension.`
# Solution (found here: http://calvinx.com/2012/12/05/geodjango-postgis-test-databases/):

sudo 2>/dev/null -u postgres psql -c "CREATE DATABASE template_postgis ENCODING='utf-8';"
sudo 2>/dev/null -u postgres psql -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"
sudo 2>/dev/null -u postgres psql -d template_postgis -f $POSTGIS_SQL_PATH/postgis.sql
sudo 2>/dev/null -u postgres psql -d template_postgis -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql
sudo 2>/dev/null -u postgres psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
sudo 2>/dev/null -u postgres psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
sudo 2>/dev/null -u postgres psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
