#!/bin/bash

# Small script to configure Django 'tledb' application

create_secret() {
  # Creates the secrets file for Django with the given key
  # $1 : path to the secrets file to be created
  # $2 : secret key to be stored

  filestr=$"
{
  \"secret_key\": \"$2\"
}
  "

  echo "$filestr" > $1

}

source 'config/scripts.config'
source "$VENV_ACTIVATE"

# 1) create secret key
key="$( python $django_skg )"
create_secret "$DJANGO_SECRETS" "$key"

# 2) migrate the database and create superuser
cd tledb
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
cd ..

deactivate
