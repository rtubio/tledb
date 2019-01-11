#!/bin/bash

# Small script for the installation of the dependencies for open-elevation
# It basically creates the right virtual environment and adds to exports
# necessary to install GDAL

####################
# IMPORTANT: This script is thought to be invoked from the ROOT of the project.
####################


source 'config/scripts.config'

# 0) Create required directories
mkdir -p "$SECRETS"
mkdir -p "$CELERY_LOGS"
mkdir -p "$STATIC_DIR"

# 1) Install Debian packages
sudo apt update && sudo apt -y full-upgrade
echo ">>> PWD = $(pwd)"
sudo apt -y install $(grep -vE "^\s*#" "$PACKAGES_FILE" | tr "\n" " ")

# 2) Setup virtual environment
[[ ! -d "$VENV_DIR" ]] && {
  virtualenv --python=python3 "$VENV_DIR"
  source "$VENV_ACTIVATE"
  pip install -r "$REQUIREMENTS_FILE"
  python scripts/django-generate-secretkey.py > "$DJANGO_SECRETS"
  deactivate
}

# 3) Configure the database
bash "$database_sh"

# 5) Configure Django
bash "$django_sh"

# 6) Setup supervisor configuration
sudo bash "$celery_sh"
sudo bash "$gunicorn_sh"

# 7) Configure NGINX
sudo bash "$nginx_sh"
