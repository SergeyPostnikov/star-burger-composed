#!/bin/bash
source .env
echo 'start git pull'
git pull
echo 'migrate'
python manage.py migrate
echo 'reload star-burger daemon'
systemctl restart star-burger

echo 'deploy completed'

