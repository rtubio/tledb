#!/bin/bash
#
# This script is intended to be used to set up a testing environment for tledb.
#
# author : rtpardavila@gmail.com

####################
# IMPORTANT: This script is thought to be invoked from the ROOT of the project.
####################

source 'conf/paths.conf'

source "$gen_django_skg_sh"
source "$gen_mail_file"
source "$gen_celery_conf"

source "$setup_dev_env"
source "$setup_os_packages"

echo "「インフォ」Setting up local development environment..."

# 0) Create required directories
mkdir -p "$LOGS_D"
mkdir -p "$SECRETS_D"
mkdir -p "$STATIC_D"
mkdir -p "$RUN_D"

# 1) A development environment is created, although in the docker container it will not be necessary.
[[ ! -f "$VENV_ACTIVATE" ]] && {
    echo "「インフォ」Python environment unavailable, installing..."
    setup_os_packages "$PACKAGES_FILE"
    setup_dev_env "$REQUIREMENTS_FILE" "$VENV_D" "$VENV_ACTIVATE"
}

# 1) Configure Django
source "$VENV_ACTIVATE"
create_secret_django "$DJANGO_SECRETS" "$( python $gen_django_skg_py )"
create_secret_mail "$MAIL_SECRETS" 'localhost' '6666' 'test' 'test'
create_celery_conf "$DJANGO_CELERY_CONF"
deactivate
