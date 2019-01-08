#!/bin/bash

# Small script for the installation of the dependencies for open-elevation
# It basically creates the right virtual environment and adds to exports
# necessary to install GDAL

####################
# IMPORTANT: This script is thought to be invoked from the ROOT of the project.
####################


source "config/scripts.config"

# 1) Install Debian packages

sudo apt update && sudo apt -y full-upgrade
echo ">>> PWD = $(pwd)"
sudo apt -y install $(grep -vE "^\s*#" "$PACKAGES_FILE" | tr "\n" " ")

# 2) Setup virtual environment

[[ ! -d "$VENV_DIR" ]] && {

  virtualenv --python=python3 "$VENV_DIR"
  source "$VENV_ACTIVATE"

  pip install -r "$REQUIREMENTS_FILE"

  deactivate

}
