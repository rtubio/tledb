#!/bin/bash

# Small script to configure Django 'tledb' application


source 'config/scripts.config'
source "$VENV_ACTIVATE"
source "$django_skg_file"
source "$gen_celery_conf"

# 1) create secret key
key="$( python $django_skg )"
create_secret "$DJANGO_SECRETS" "$key"

# 2) create configuration for Celery / rabbitmq
create_celery_conf "$DJANGO_CELERY_CONF"

# 3) migrate the database and create superuser
cd tledb
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
cd ..

deactivate
