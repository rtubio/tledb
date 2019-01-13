#!/bin/bash

cd "/opt/services/tledb/tledb"
python manage.py migrate
python manage.py collectstatic --no-input

/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
