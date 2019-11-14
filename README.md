[![pipeline-status](https://git.sinntern.de/django/landmatrix/badges/master/pipeline.svg)](https://git.sinntern.de/django/landmatrix/commits/master)
[![coverage-report](https://git.sinntern.de/django/landmatrix/badges/master/coverage.svg)](https://git.sinntern.de/django/landmatrix/commits/master)
[![python version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[[![Read the Docs](https://img.shields.io/readthedocs/landmatrix)](http://landmatrix.rtfd.io/)

# Land Matrix

The Land Matrix is a global and independent land monitoring initiative that promotes\
transparency and accountability in decisions over land and investment.

The website is our Global Observatory - an open tool for collecting and visualising
information about large-scale land acquisitions.

See https://landmatrix.org for more information.

## Installation

### Databases
You will need PostgreSQL including PostGIS. This project will **not** work with anything else.

```bash
sudo apt install postgresql-10 postgresql-10-postgis-scripts
sudo -u postgres psql -c "CREATE USER landmatrix WITH PASSWORD 'landmatrix'"
sudo -u postgres psql -c "CREATE DATABASE landmatrix WITH OWNER landmatrix"
sudo -u postgres psql landmatrix -c "CREATE EXTENSION postgis"
```

You also need [ElasticSearch Version 5](https://www.elastic.co/de/downloads/past-releases/elasticsearch-5-0-0)

### Python
To install the requirements into a virtual environment this project uses [Poetry](https://poetry.eustace.io/).
Either just run `pip3 install --user poetry` or see poetry's alternative
 [installation methods](https://github.com/sdispater/poetry#installation).


Once you have poetry, install the virtual environment and the dependencies:
```bash
poetry install
```

### Javascript

Get yarn (or npm), but we recommend yarn:

```bash
# Install yarn (https://yarnpkg.com/lang/en/docs/install/#debian-stable)
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update && sudo apt install yarn
```

### Custom settings via .env

Any kind of settings you need to set for your system should happen in the `.env` file.
Usually you should **not** have to edit files in `settings/`.
```bash
cp .env.example .env
$EDITOR .env  # make changes fitting your host system
```

### Create the basic structure
```bash
poetry run doit initial_setup
```
Check the `dodo.py` file and the [pydoit](https://pydoit.org/) documentation to see what happens here.


### Management commands

Jobs that are run regularly using cron:

* `python manage.py populate_activities`: populates the activities with common used attributes
* `python manage.py update_elasticsearch`: Updates all documents within the elasticsearch index.<br>
    It is recommended to run populate_activities before.

Other jobs:

* `python manage.py check_export`: checks if the given export file (XLSX) has any errors (for internal QA)
* `python manage.py get_not_public_reason`: checks why deal is not public
* `python manage.py load_country_geometries`: populates the countries with shape geometries (from biogeo.ucdavis.edu)
* `python manage.py populate_countries`: populates the country bounding boxes for zooming in the map.



## Structure and Apps schema

* **apps/**
    * **api**: Well, the API. Mostly internal at this point.
    * **charts**: Views for the Charts section
    * **editor**: Mainly Views for the Editor section
    * **feeds**: RSS/Atom feeds for activities
    * **grid**: Views for the Grid (or Data) section
    * **landmatrix**: All the relevant **models**
    * **map**: Some Views for the Map
    * **notifications**: Email notifications
    * **ol3_widgets**: OpenLayers 3 widgets (**old** 😔)
    * **public_comments**: ThreadedComments adapter
    * **wagtailcms**: Everything connected to the CMS
* **config**: Django settings, urls and locale
* **docs**: Make files for landmatrix.readthedocs.io
* **media**: Django [media folder](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-MEDIA_ROOT)
* **templates**: Root level Django template folder


## Development

Code is formatted with **black**, we use **pylint** to some extend, as well as **isort**.
The projects includes integration and unit tests.

For [up-to-date information](https://en.wikipedia.org/wiki/Self-documenting_code) see:

* `.gitlab-ci.yml`
* `pyproject.toml`
* `.coveragerc`
* `.pylintrc`
