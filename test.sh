#!/bin/bash

poetry run ./manage.py shell << E=O=F
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()
if not User.objects.filter(username='shakespeare').exists():
 will = User.objects.create_superuser('shakespeare', 'william@shakespeare.dev', 'hamlet4eva')
 admins = Group.objects.create(name='Administrators')
 will.groups.set([admins])
 will.save()
E=O=F

echo "Waiting django to launch on 8000..."
poetry run ./manage.py runserver &
RUNSERVER_PID=$!
while ! nc -z localhost 8000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
echo "Django launched"


npx playwright test

kill $RUNSERVER_PID
sleep 1

