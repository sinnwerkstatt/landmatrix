#!/bin/bash

# 1. Install django
poetry install

# 2. Install frontend
(cd newfront && npm install)

# 3. Setup django test env
doit reset_db
doit initial_setup
./manage.py create_playwright_test_users
