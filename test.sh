#!/bin/bash

poetry run ./manage.py runserver &
RUNSERVER_PID=$!

echo "Waiting django to launch on 8000..."
while ! nc -z localhost 8000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
echo "Django launched"

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('shakespeare', 'william@shakespeare.dev', 'hamlet4eva')" | poetry run ./manage.py shell

npx playwright test

kill $RUNSERVER_PID
sleep 1

