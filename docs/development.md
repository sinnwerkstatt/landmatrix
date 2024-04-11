# Development

Code is formatted with **black**, we use **pylint** to some extent, as well as **isort**.
The project includes integration and unit tests.

For [up-to-date information](https://en.wikipedia.org/wiki/Self-documenting_code) see:

* `.gitlab-ci.yml`
* `pyproject.toml`
* `.coveragerc`
* `.pylintrc`


### Ubuntu requirements

```bash
# For pillow (https://pillow.readthedocs.io/en/latest/installation.html#building-on-linux)
sudo apt install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev
# for geostuff
sudo apt install gdal-bin postgresql-13-postgis-3
```

### Add i18n strings to Frontend

1. Make sure the string is encapsulated by `$_('string')`
2. ```shell
   cd plumbing
   poetry run python ./find_i18n.py
   ```
3. `poetry run ./manage.py make_messages -a`
   **Watch out!**  Don't use Django's `makemessages`.
4. `poetry run doit compilemessages`

### Register existing model for i18n

Model translations are handled by `django-modeltranslation`.

1. Register model as described in the [docs](https://django-modeltranslation.readthedocs.io/en/latest/registration.html).
2. Create and run migrations.
   ```shell
   ./manage.py makemigrations`
   ./manage.py migrate`
   ```
3. Map old to new fields: `./manage.py update_translation_fields`


### Restore DB from dump

```shell
zcat landmatrix.sql.gz | psql -h localhost -U landmatrix landmatrix
./manage.py migrate
```

### Testing

#### Backend / Django

* Run tests via: `poetry run pytest apps`
* Show what is done under the hood (being very verbose and capturing no output): `poetry run pytest apps -s -vv`
* With coverage: `poetry run pytest apps --cov=apps`
* To force new db creation after migrating: `poetry run pytest apps --create-db`
* Start pytest in watch mode: `poetry run ptw apps`
