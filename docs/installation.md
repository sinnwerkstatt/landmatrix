# Installation

### Databases
You will need PostgreSQL including PostGIS. This project will **not** work with anything else.

```bash
#ubuntu 18.04
sudo apt install postgresql-10 postgresql-10-postgis-scripts
#ubuntu 20.04
sudo apt install postgresql-12 postgresql-12-postgis-3-scripts

# creation of the relevant database with extension
sudo -u postgres psql -c "CREATE USER landmatrix WITH PASSWORD 'landmatrix'"
sudo -u postgres psql -c "CREATE DATABASE landmatrix WITH OWNER landmatrix"
sudo -u postgres psql landmatrix -c "CREATE EXTENSION postgis"
```

### Python
To install the requirements into a virtual environment this project uses [Poetry](https://poetry.eustace.io/).
Either just run `pip3 install --user poetry` or see poetry's alternative
 [installation methods](https://github.com/sdispater/poetry#installation).


Once you have poetry, install the virtual environment and the dependencies:
```bash
poetry install
```

### Javascript

Get `npm`; just follow https://nodejs.org/.


### Custom settings via `.env`

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
