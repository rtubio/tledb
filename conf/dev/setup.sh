#!/bin/bash
#
# This script is intended to be used to set up a testing environment for tledb.
#
# author : rtpardavila@gmail.com

####################
# IMPORTANT: This script is thought to be invoked from the ROOT of the project.
####################

source 'conf/paths.conf'
source "$PRO_PATHS"

source "$gen_django_skg_sh"
source "$gen_mail_file"
source "$gen_celery_conf"

# 0) Create required directories
mkdir -p "$SECRETS_D"
mkdir -p "$LOGS_D"
mkdir -p "$STATIC_D"

# 1) Configure Django
create_secret_django "$DJANGO_SECRETS" "$( python $gen_django_skg_py )"
create_secret_mail "$MAIL_SECRETS" 'localhost' '6666' 'test' 'test'
create_celery_conf "$DJANGO_CELERY_CONF"

deactivate
