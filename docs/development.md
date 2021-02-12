# Development

Code is formatted with **black**, we use **pylint** to some extend, as well as **isort**.
The projects includes integration and unit tests.

For [up-to-date information](https://en.wikipedia.org/wiki/Self-documenting_code) see:

* `.gitlab-ci.yml`
* `pyproject.toml`
* `.coveragerc`
* `.pylintrc`


### Add i18n strings to Frontend

1. Make sure the string is encapsulated by `vue-i18n`-helper: `$t('string')`
2. Copy string to `/config/frontend_i18n_strings.py`
3. `poetry run ./manage.py make_messages`
   **Watch out!**  Don't use Django's `makemessages`.
4. `poetry run doit compilemessages`
