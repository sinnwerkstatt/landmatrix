Installation
============

1. Install system packages (Debian)

.. code-block:: shell

    $ sudo apt-get install postgresql-9.4-postgis-scripts postgresql-9.4-postgis-2.1 postgresql-9.4 postgresql-client-9.4 postgresql-contrib-9.4 \
                     virtualenvwrapper python3-psycopg2 libpq-dev npm

2. Setup a virtual environment for Python3.4 including the postgres driver (Virtualenv):

.. code-block:: shell

    $ mkvirtualenv landmatrix --system-site-packages -p /usr/bin/python3.4
    $ workon landmatrix

3. Install Django requirements (PIP):

If you intend to do ANY development on the frontend/backend, use the requirements-dev.txt in the next step, it will
include the default requirements.txt:

.. code-block:: shell

    $ pip install -r requirements.txt

4. Set up the database, user and postgis (Init script):

.. code-block:: shell

    $ ./init.sh

5. Create settings file and adapt database settings:

.. code-block:: shell

    $ cp landmatrix/settings.py.dist landmatrix/settings.py

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
===

The API documentation can be found at https://dev.landmatrix.org/api/


Tests
=====

The projects includes integration and unit tests.
The tests are run using django-nose in the background.
The following command runs the test cases:

.. code-block:: shell

    $ python manage.py test
