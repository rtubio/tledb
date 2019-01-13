#!/bin/bash

# Small script to configure Django 'tledb' application


create_secret() {
  # Creates the secrets file for Django with the given key
  # $1 : path to the secrets file to be created
  # $2 : secret key to be stored

  echo "
{
  \"secret_key\": \"$2\"
}
  " > $1

}


create_celery_conf() {
  # Creates the configuration for Celery / RabittMQ
  # $1 : path to the secrets file to be created

  echo "
{
  \"broker\": \"amqp://localhost\",
  \"backend\": \"django-db\"
}
  " > $1

}


source 'config/scripts.config'
source "$VENV_ACTIVATE"

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
