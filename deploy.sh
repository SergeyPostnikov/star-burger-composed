#!/bin/bash

set -e

# Цвет ANSI для фиолетового текста
PURPLE='\e[35m'
# Сброс цвета (вернуть к стандартному)
RESET='\e[0m'

echo -e "${PURPLE}Load .env${RESET}"
source .env

echo -e "${PURPLE}Pulling changes${RESET}"
git pull

echo -e "${PURPLE}Apply migrations${RESET}"
/opt/star-burger/env/bin/python manage.py migrate --noinput

echo -e "${PURPLE}Collect static${RESET}"
/opt/star-burger/env/bin/python manage.py collectstatic --noinput --clear

echo -e "${PURPLE}Installing js packages${RESET}"
npm ci --dev

echo -e "${PURPLE}Parcel build bundles${RESET}"
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./" &

echo -e "${PURPLE}Reload star-burger daemon${RESET}"
systemctl restart star-burger

echo -e "${PURPLE}Send deploy info to rollbar${RESET}"

COMMIT_HASH=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: $ROLLBAR_KEY" \
     -H "Content-Type: application/json" \
     -X POST 'https://api.rollbar.com/api/1/deploy' \
     -d "{\"environment\": \"production\", \"revision\": \"$COMMIT_HASH\", \"status\": \"succeeded\"}"

echo -e "\n${PURPLE}deploy completed${RESET}"

