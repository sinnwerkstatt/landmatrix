[![pipeline-status](https://git.sinntern.de/django/landmatrix/badges/master/pipeline.svg)](https://git.sinntern.de/django/landmatrix/commits/master)
[![coverage-report](https://git.sinntern.de/django/landmatrix/badges/master/coverage.svg)](https://git.sinntern.de/django/landmatrix/commits/master)
[![python version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Read the Docs](https://img.shields.io/readthedocs/landmatrix)](http://landmatrix.rtfd.io/)

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


## Landmatrix API Documentation

The Landmatrix API is available at [dev.landmatrix.org/graphql/](dev.landmatrix.org/graphql/) and provides deal as well as investor data sets.
The API requires you to write your queries in [GraphQL syntax](https://graphql.org/learn/) and returns the matching data sets as a [JSON](https://www.json.org/json-en.html) formatted response.

_API rate limiting?_

### Data types and fields
#### Deals
_A deal is an transaction associated with a particular piece of land or area._

The deal data schema including all available fields can be found in the `Schema` section at [dev.landmatrix.org/graphql/](dev.landmatrix.org/graphql/).

#### Investors
_Investors are people or associations who or which are associated with a land deal._

The Investor data schema including all available fields can be found in the `Schema` section at [dev.landmatrix.org/graphql/](dev.landmatrix.org/graphql/).


### Query examples

#### Deal data by ID

If you want to recieve a specific deal by ID you can pass the ID as an argument to the query. In this case you are querying for the data type `deal`.
```
{
  deal(id: 3) {
    geojson
  }
}
``` 
will return 
```
{
  "data": {
    "deal": {
      "geojson": {
        "type": "FeatureCollection",
        "features": [
          {
            "type": "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": [
                93.98784269999999,
                19.810093
              ]
            },
            "properties": {
              "name": "Rakhine, Myanmar",
              "type": "point"
            }
          }
        ]
      }
    }
  }
}
```

_Deal IDs can for example be found [in the data section](https://landmatrix.org/data/) of the Landmatrix web application._

#### All deal data

Data on all deals available can be recieved by querying for `deals`.
```
{
  deals(limit: 5) {
    geojson
  }
}
```
for example is going to return data of the _first_ 5 deals.


```
{
  deals(limit: 5, sort: "target_country") {
    geojson
  }
}
```
returns data for of the _first_ 5 deals sorted alphabetically by target country (asc).

#### Investor data by ID

To find a specific investor by ID simply pass the ID to the `investor` query:
```
{
  investor(id: 1010) {
    id
    name
    country {
      name
    }
  }
}
```
is going to return 
```
{
  "data": {
    "investor": {
      "id": 1010,
      "name": "I.D.C Investment",
      "country": {
        "name": "Denmark"
      }
    }
  }
}
```

#### All investor data

Data on all investors available can be recieved by querying for `investors`.
```
{
  investors(limit: 5) {
    id
    name
  }
}
```
for example is going to return `id` and `name` of the _first_ 5 investors.


### Filters

In most use cases you may want to specify some fields and conditions you want to have your query results filtered by.
You can pass a `filter` array to your query as an argument. More information on GraphQL filtering can be found [on GRANDstack](https://grandstack.io/docs/graphql-filtering/#filter-argument).

#### Filter examples

The query
```
query Size($timestamp: [Filter]) {
  deals(filters: $timestamp, limit: 3) {
    id
    deal_size
  }
}
```
with the filter
```
{
  "timestamp": [
      {
        "field": "timestamp", "operation": "GE", "value": "2020-03-02"
      },
 	 ]
}
```
defined in the `Query Variables` section is going to return the following JSON:
```
{
  "data": {
    "deals": [
      {
        "id": 3,
        "deal_size": 20234
      },
      {
        "id": 4,
        "deal_size": 0
      },
      {
        "id": 8,
        "deal_size": 0
      }
    ]
  }
}
```

If you want to apply a filter without using the sandbox provided at [dev.landmatrix.org/graphql/](dev.landmatrix.org/graphql/) you can directly incorporate the filter array into your query like this:
```
{
  deals(filters: { field: "timestamp", operation: GE, value: "2020-03-02" }) {
    id
    deal_size
  }
}
```

You can also chain filters using `AND` or `OR` operators:

```
# TODO: figure out filter chaining...
```

#### Logical operators

Available logical operators are:

* `EQ`: equals
* `IN`: in/part of
* `LT`: less than
* `LE`: less or equal than
* `GT`: greater than
* `GE`: greater or equal than
