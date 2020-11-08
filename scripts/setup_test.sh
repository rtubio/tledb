#!/bin/bash
#
# This script is intended to be used to set up a testing environment for tledb.
#
# author : rtpardavila@gmail.com

####################
# IMPORTANT: This script is thought to be invoked from the ROOT of the project.
####################


source 'config/scripts.config'
source "$django_skg_file"
source "$gen_mail_file"
source "$gen_celery_conf"

# 0) Create required directories
mkdir -p "$SECRETS"
mkdir -p "$CELERY_LOGS"
mkdir -p "$STATIC_DIR"

# 1) Configure Django
key="$( python $django_skg )"
create_secret "$DJANGO_SECRETS" "$key"
create_mail_secrets "$MAIL_SECRETS" 'localhost' '6666' 'test' 'test'
create_celery_conf "$DJANGO_CELERY_CONF"

# ACTIVATE Only if necessary for testing
# 2) migrate the database and create superuser
# cd tledb
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py collectstatic
# cd ..
