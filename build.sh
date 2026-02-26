#!/usr/bin/env bash
set -e

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py wait_for_db
python manage.py migrate