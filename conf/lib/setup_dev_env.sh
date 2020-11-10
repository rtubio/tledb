#!/bin/bash

setup_dev_env() {

    REQUIREMENTS_FILE="$1"
    VENV_D="$2"
    VENV_ACTIVATE="$3"

    install_os_packages

    echo "「インフォ」Python environment does not exist, creating..."

    python3 -m virtualenv --python python3 "$VENV_D"
    source "$VENV_ACTIVATE"
    pip install -r "$REQUIREMENTS_FILE"
    deactivate

}
