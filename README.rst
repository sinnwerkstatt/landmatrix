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

If you intend to develop on the frontend, you'll probably want livereload:
$ npm install gulp gulp-livereload  gulp-watch

Setup a virtual environment for Python3.4 including the postgres driver:
$ mkvirtualenv landmatrix --system-site-packages -p /usr/bin/python3.4
$ workon landmatrix

Install Django requirements via pip:
If you intend to do ANY development on the frontend/backend, use the requirements-dev.txt in the next step, it will
include the default requirements.txt:
$ pip install -r requirements.txt

Set up the database, user and postgis:

$ ./init.sh

If you want to restore old data to the database (see below), now would be a good time.
After the database is ready, Run the migrations - just to make sure:

$ python manage.py migrate

We upgraded to Sass, so compilation of the stylesheets has become a necessity (until the builtin automation is fixed):

$ python manage.py compilescss

This will generate a "main.css" which should already be included in the repository. You'll mostly need this to
regenerate after changes to the CSS.

Also collecting the statics is essential:

$ python manage.py collectstatic

Run the server:

$ python manage.py runserver


Manage commands
---------------
$ python manage.py check_export
$ python manage.py clean_activityattributegroups
$ python manage.py compare_lists
$ python manage.py deals_with_multiple_primary_investors
$ python manage.py elasticsearch_test
$ python manage.py get_investor_duplicates
$ python manage.py get_not_public_reason
$ python manage.py link_comments
$ python manage.py load_country_geometries
$ python manage.py populate_activities
$ python manage.py populate_activity_changesets
$ python manage.py populate_countries
$ python manage.py populate_operational_companies
$ python manage.py primary_investors_with_different_countries
$ python manage.py read_new_countries
$ python manage.py update_elasticsearch


Structure and Apps schema
-------------------------
- api
- charts
- docs
- editor
- feeds
- from_v1
- grid
- landmatrix
    - default_settings.py
    - settings.py
- lo
- locale
- map
- media
- notifications
- ol3_widgets
- public_comments
- static
- templates
- wagtailcms
manage.py
requirements.txt
fabfile.py

API
---

Tests
-----