#!/bin/bash

PG_USER=${PG_USER:=landmatrix}
PG_PASSWD=${PG_PASSWD:=landmatrix}
PG_DB=${PG_DB:=landmatrix_2}
DROP_DB=${DROP_DB:=no}

# ensure that postgresql and psql client are installed
which psql >/dev/null || \
    sudo apt-get install postgresql postgresql-contrib postgresql-client postgresql-server-dev-9.4 libpq-dev

# ensure Postgres user exists
sudo 2>/dev/null -u postgres psql -d postgres -c \\du | grep -q "${PG_USER}" || \
    sudo 2>/dev/null -u postgres psql -s postgres -c "create user $PG_USER password '$PG_PASSWD';"

# ensure Postgres user has an entry in ~/.pgpass for passwordless login to psql client
grep -q $PG_USER $HOME/.pgpass || \
    echo 'localhost:5432:*:'"$PG_USER:$PG_PASSWD" >> $HOME/.pgpass
    
# ensure Postgres user can create (and drop) DBs
sudo 2>/dev/null -u postgres psql -d postgres -c "ALTER USER $PG_USER CREATEDB;"

# Create DB, grant full access to $PG_USER and add HStore extension
test $DROP_DB == 'yes' && \
    sudo 2>/dev/null -u postgres psql -d postgres -c "DROP DATABASE IF EXISTS $PG_DB;" -e

createdb -U $PG_USER $PG_DB -e && \
    sudo 2>/dev/null -u postgres psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $PG_DB TO $PG_USER;" -e && \
    sudo 2>/dev/null -u postgres psql -d $PG_DB -c "CREATE_EXTENSION hstore;" -e && \
    sudo 2>/dev/null -u postgres psql -d template1 -c 'create extension hstore;'

# Ensure test DB is gone
psql -U $PG_USER -d $PG_DB -c "DROP DATABASE IF EXISTS test_$PG_DB;"