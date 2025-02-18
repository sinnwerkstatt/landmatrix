#!/bin/bash

# 1. Install django
uv sync

# 2. Install frontend
(cd frontend && pnpm install && pnpm run build)

# 3. Setup django test env
doit reset_db
doit initial_setup
./manage.py create_playwright_test_users

# 4. Update playwright
npx playwright install
