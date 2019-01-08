#!/bin/bash

NAME='tledb'
CELERY_SUPERVISOR_CFG='/etc/supervisor/conf.d/tledb-celery.conf'

[[ $( whoami ) == 'root' ]] || {
    echo 'Need to be <root>, exiting...' && exit -1
}

[[ -f "$CELERY_SUPERVISOR_CFG" ]] && {
  echo "[WARN] <$CELERY_SUPERVISOR_CFG> exists, keeping a backup copy"
  mv -f "$CELERY_SUPERVISOR_CFG" "$CELERY_SUPERVISOR_CFG.bak"
}

echo '[program:tledb-celery]' > "$CELERY_SUPERVISOR_CFG"
echo "command=$(pwd)/.tledb/bin/celery worker -A $NAME --loglevel=INFO" >> "$CELERY_SUPERVISOR_CFG"
echo "directory=$(pwd)/tledb" >> "$CELERY_SUPERVISOR_CFG"
echo "user=nobody" >> "$CELERY_SUPERVISOR_CFG"
echo "numprocs=1" >> "$CELERY_SUPERVISOR_CFG"
echo "stdout_logfile=$(pwd)/logs/celery.log" >> "$CELERY_SUPERVISOR_CFG"
echo "stderr_logfile=$(pwd)/logs/celery.log" >> "$CELERY_SUPERVISOR_CFG"
echo "autostart=true" >> "$CELERY_SUPERVISOR_CFG"
echo "autorestart=true" >> "$CELERY_SUPERVISOR_CFG"
echo "startsecs=10" >> "$CELERY_SUPERVISOR_CFG"

# Need to wait for currently executing tasks to finish at shutdown.
# Increase this if you have very long running tasks.
echo "stopwaitsecs=600" >> "$CELERY_SUPERVISOR_CFG"
echo "stopasgroup=true" >> "$CELERY_SUPERVISOR_CFG"

# Set Celery priority higher than default (999)
# so, if rabbitmq is supervised, it will start first.
echo "priority=1000" >> "$CELERY_SUPERVISOR_CFG"
