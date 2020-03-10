#!/bin/bash

poetry run doit reset_db || exit
zcat landmatrix-2020.02.11.sql.gz | PGPASSWORD="landmatrix" psql -U landmatrix landmatrix
poetry run ./manage.py migrate
poetry run ./manage.py loaddata apps/greennewdeal/fixtures/countries_and_regions.json
poetry run ./manage.py loaddata apps/greennewdeal/fixtures/currency.json
