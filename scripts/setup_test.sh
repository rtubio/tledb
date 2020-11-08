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

# 0) Create required directories
mkdir -p "$SECRETS"
mkdir -p "$CELERY_LOGS"
mkdir -p "$STATIC_DIR"

# 1) Configure Django
key="$( python $django_skg )"
create_secret "$DJANGO_SECRETS" "$key"
create_mail_secrets "$MAIL_SECRETS" 'localhost' '6666' 'test' 'test'
