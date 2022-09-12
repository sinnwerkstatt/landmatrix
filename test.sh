#!/bin/bash

# 1. Install django
poetry install

# 2. this assumes a fresh empty database
poetry run doit initial_setup

# 3. create test user:
poetry run ./manage.py shell << E=O=F
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()

if not User.objects.filter(username='shakespeare').exists():
  will = User.objects.create_superuser('shakespeare', 'william@shakespeare.dev', 'hamlet4eva')
  will.level = 3
  cms_editors, _ = Group.objects.get_or_create(name="CMS Global (Editors)")
  will.groups.set([cms_editors])
  will.save()

if not User.objects.filter(username='test_editor').exists():
  user = User.objects.create_user('test_editor', 'editor@test.dev', 'love2edit')
  user.level = 2
  user.save()

if not User.objects.filter(username='test_reporter').exists():
  user = User.objects.create_user('test_reporter', 'reporter@test.dev', 'love2report')
  user.level = 1
  user.save()
E=O=F

# 4. Start Django
echo "Waiting for Django to launch on 8000..."
poetry run ./manage.py runserver &
RUNSERVER_PID=$!
while ! nc -z localhost 8000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
echo "Django launched"

# 5. Start svelte vite
echo "Waiting for Svelte to launch on 3000..."
cd newfront
npm install
npm run build
npm run preview &
APP_PID=$!
while ! nc -z localhost 3000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
cd ..

# 6. Start caddy
echo "Waiting for Caddy to launch on 9000..."
npm run caddy &
CADDY_PID=$!
while ! nc -z localhost 9000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done

# 7. Run tests
npx playwright test tests

kill $CADDY_PID
kill $APP_PID
kill $RUNSERVER_PID

sleep 1

