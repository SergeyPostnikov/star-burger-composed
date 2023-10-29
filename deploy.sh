#!/bin/bash

set -e

echo 'load .env'
source .env

echo 'start git pull'
git pull
echo 'migrate'
/opt/star-burger/env/bin/python manage.py migrate
echo 'collectstatic'
/opt/star-burger/env/bin/python manage.py collectstatic
echo 'installing js packages'
npm ci --dev

echo 'parcel build bundles'

./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./" &

echo 'reload star-burger daemon'
systemctl restart star-burger

echo 'send deploy info to rollbar'

COMMIT_HASH=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: $ROLLBAR_KEY" \
     -H "Content-Type: application/json" \
     -X POST 'https://api.rollbar.com/api/1/deploy' \
     -d "{\"environment\": \"production\", \"revision\": \"$COMMIT_HASH\", \"status\": \"succeeded\"}"

echo 'deploy completed'

