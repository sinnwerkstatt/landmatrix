#!/bin/bash

# 1. Install django
poetry install

# 2. Setup django test env
doit reset_db
doit initial_setup
./manage.py create_playwright_test_users

# 3 Build the frontend
(cd newfront && npm install && npm run build)

# 4. Start app
concurrently npm:backend npm:frontend npm:caddy > /dev/null &
PID=$!

# 5. Wait for app to be responsive
while ! nc -z localhost 3000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
echo 'Django online'

while ! nc -z localhost 8000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
echo 'Frontend online'

while ! nc -z localhost 9000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
echo 'Caddy online'


# 6. Run tests
npx playwright test tests/login.spec.ts
npx playwright test tests/cms.spec.ts
npx playwright test tests/roles.spec.ts
npx playwright test tests/create-deal-investor.spec.ts
npx playwright test tests/workflow.spec.ts

# 7. Cleanup
kill $PID
sleep 2

