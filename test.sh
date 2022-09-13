#!/bin/bash

# 1. Start test environment
concurrently npm:backend npm:frontend npm:caddy &
PID=$!

while ! nc -z localhost 8000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
while ! nc -z localhost 9000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
while ! nc -z localhost 3000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done

# 2. create test user:
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

# 3. Run tests
npx playwright test tests/login.spec.ts
#npx playwright test tests/roles.spec.ts
#npx playwright test tests/workflow.spec.ts

# 4. Cleanup
kill $PID
sleep 2

