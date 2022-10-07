#!/bin/bash

# 1. Start app
# The output is discarded to see the actual test results.
# If you want to see the output run `npm run dev:test` in one terminal
# and `npm run playwright` in another terminal.
echo 'Starting backend, frontend (dev) and proxy'
concurrently npm:backend npm:frontend npm:caddy > /dev/null &
PID=$!

# 2. Wait for app to be responsive
echo 'Waiting for backend'
while ! nc -z localhost 8000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
echo 'Django online'

echo 'Waiting for frontend'
while ! nc -z localhost 3000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
echo 'Frontend online'

echo 'Waiting for proxy'
while ! nc -z localhost 9000; do
  sleep 0.3 # wait for 3/10 of the second before check again
done
echo 'Caddy online'


# 3. Run tests
npm run playwright
success=$?

# 4. Cleanup
kill $PID
sleep 2

exit $success
