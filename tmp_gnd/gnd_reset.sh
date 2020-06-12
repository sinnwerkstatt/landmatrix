#!/bin/bash

poetry run doit reset_db || exit
zcat landmatrix.sql.gz | PGPASSWORD="landmatrix" psql -U landmatrix landmatrix -h localhost
poetry run ./manage.py migrate
poetry run ./manage.py loaddata apps/greennewdeal/fixtures/countries_and_regions.json
poetry run ./manage.py loaddata apps/greennewdeal/fixtures/currency.json
