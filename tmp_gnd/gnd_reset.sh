#!/bin/bash

poetry run doit reset_db || exit
zcat landmatrix.sql.gz | PGPASSWORD="landmatrix" psql -U landmatrix landmatrix -h localhost
poetry run ./manage.py migrate

poetry run ./manage.py sync_investors
poetry run ./manage.py sync_deals
