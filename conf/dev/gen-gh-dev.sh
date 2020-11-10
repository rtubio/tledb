#!/bin/bash

source 'conf/paths.conf'

echo "tledb.PKGS_PY=$REQUIREMENTS_FILE" >> "$GH_ENV"
echo "tledb.CONF_COVERAGE=$COVERAGE_CONF" >> "$GH_ENV"
