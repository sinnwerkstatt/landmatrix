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

1. Make sure the string is encapsulated by `vue-i18n`-helper: `$t('string')`
2. Copy string to `/config/frontend_i18n_strings.py`
3. `poetry run ./manage.py make_messages`
   **Watch out!**  Don't use Django's `makemessages`.
4. `poetry run doit compilemessages`
