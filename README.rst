[![pipeline status](https://git.sinntern.de/django/landmatrix/badges/master/pipeline.svg)](https://git.sinntern.de/django/landmatrix/commits/master)
[![coverage report](https://git.sinntern.de/django/landmatrix/badges/master/coverage.svg)](https://git.sinntern.de/django/landmatrix/commits/master)

Landmatrix
==========


Installation
------------

System packages (Ubuntu/Debian)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ sudo apt install postgresql-10-postgis-scripts

    # Install yarn (https://yarnpkg.com/lang/en/docs/install/#debian-stable)
    $ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    $ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
    $ sudo apt-get update && sudo apt-get install yarn


Database
~~~~~~~~

You will need PostgreSQL including PostGIS. This project will **not** work with anything else.

.. code-block:: shell

  $ sudo -u postgres psql -c "CREATE USER landmatrix WITH PASSWORD 'landmatrix'"
  $ sudo -u postgres psql -c "CREATE DATABASE landmatrix WITH OWNER landmatrix"
  $ sudo -u postgres psql landmatrix -c "CREATE EXTENSION postgis"


Python virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

This can be done in several ways, but we recommend `Pipenv <https://docs.pipenv.org/en/latest/>`_.

Once you have pipenv on your system, install the dependencies:

.. code-block:: shell

  $ pipenv --sync


Custom settings via .env
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

  $ cp .env.example .env
  $ $EDITOR .env  # make changes fitting your host system



.. code-block:: shell

  $ pipenv run ./manage.py createsuperuser


old.
=====

6. Run database migrations:

After the database is ready, Run the migrations - just to make sure:

.. code-block:: shell

    $ python manage.py migrate

7. Install frontend dependencies (Bower):

.. code-block:: shell

    $ sudo npm -g install bower
    $ bower install

If you intend to develop on the frontend, you'll probably want livereload:

.. code-block:: shell

    $ npm install gulp gulp-livereload  gulp-watch


8. Compile CSS and collect static files:

.. code-block:: shell

    $ python manage.py compilescss

This will generate a "main.css" which should already be included in the repository. You'll mostly need this to
regenerate after changes to the CSS.

Then collect the static files (CSS, Javascript and images):

.. code-block:: shell

    $ python manage.py collectstatic

9. Run the server:

.. code-block:: shell

    $ python manage.py runserver


Manage commands
===============
    
Checks if the given export file (XLSX) has any errors (for internal QA).

.. code-block:: shell
    
    $ python manage.py check_export

Checks why deal is not public.

.. code-block:: shell
    
    $ python manage.py get_not_public_reason
    
Populates the countries with shape geometries (from biogeo.ucdavis.edu)
    
.. code-block:: shell
    
    $ python manage.py load_country_geometries
    
Populates the activities with common used attributes.
This command is run by a CronJob on the production system.

.. code-block:: shell
    
    $ python manage.py populate_activities

Populates the country bounding boxes for zooming in the map.

.. code-block:: shell
    
    $ python manage.py populate_countries

    
    
Updates all documents within the elasticsearch index.
This command is run by a CronJob on the production system.
It is recommended to run populate_activities before.

.. code-block:: shell
    
    $ python manage.py update_elasticsearch


Structure and Apps schema
=========================

* **api**: App providing all views for the API
* **charts**: App providing all views for the Charts section
* **docs**: Make files for landmatrix.readthedocs.io
* **editor**: App prodiving all views for the Editor section
* **feeds**: App providing RSS/Atom feeds for activities
* **from_v1**: Migration scripts for the old database
* **grid**: App providing all views for the Grid (or Data) section
* **landmatrix**: Django main application folder including settings.py file
* **locale**: Django translation files (maintained by: manage.py makemessages/compilemessages)
* **map**: App providing all views for the Map section
* **media**: Django media folder for user uploads (e.g. in CMS)
* **notifications**: App providing email notifications
* **ol3_widgets**: App providing OpenLayers 3 widgets
* **public_comments**: App providing threaded comments
* **static**: Django static folder, for CSS, Javascript and image files used by the frontend
* **templates**: Django template folder
* **wagtailcms**: App providing the CMS 
* *manage.py*: Django manage project script
* *requirements.txt*: Required python packages for PIP command
* *fabfile.py*: Configuration files for deployment using Fabric

API
---

The API documentation can be found at https://dev.landmatrix.org/api/


Tests
-----

The projects includes integration and unit tests.
The tests are run using django-nose in the background.
The following command runs the test cases:

.. code-block:: shell
    
    $ python manage.py test
