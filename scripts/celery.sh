#!/bin/bash

# TODO # check how to roll supervisor's logs!

NAME='tledb'
CELERY_BEAT_CFG='/etc/supervisor/conf.d/tledb-beat.conf'
CELERY_WORKER_CFG='/etc/supervisor/conf.d/tledb-worker.conf'

[[ $( whoami ) == 'root' ]] || {
    echo 'Need to be <root>, exiting...' && exit -1
}

# ### (1) BEAT Configuration for CELERY

[[ -f "$CELERY_BEAT_CFG" ]] && {
  echo "[WARN] <$CELERY_BEAT_CFG> exists, keeping a backup copy"
  mv -f "$CELERY_BEAT_CFG" "$CELERY_BEAT_CFG.bak"
}

echo '[program:tledb-beat]' > "$CELERY_BEAT_CFG"
echo "command=$(pwd)/.tledb/bin/celery -A $NAME beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler" >> "$CELERY_BEAT_CFG"
echo "directory=$(pwd)/tledb" >> "$CELERY_BEAT_CFG"
echo "user=$USER" >> "$CELERY_BEAT_CFG"
echo "numprocs=1" >> "$CELERY_BEAT_CFG"
echo "stdout_logfile=$(pwd)/logs/tledb-beat.log" >> "$CELERY_BEAT_CFG"
echo "stderr_logfile=$(pwd)/logs/tledb-beat.log" >> "$CELERY_BEAT_CFG"
echo "autostart=true" >> "$CELERY_BEAT_CFG"
echo "autorestart=true" >> "$CELERY_BEAT_CFG"
echo "startsecs=10" >> "$CELERY_BEAT_CFG"

# Need to wait for currently executing tasks to finish at shutdown.
# Increase this if you have very long running tasks.
echo "stopwaitsecs=600" >> "$CELERY_BEAT_CFG"
echo "stopasgroup=true" >> "$CELERY_BEAT_CFG"

# Set Celery priority higher than default (999)
# so, if rabbitmq is supervised, it will start first.
echo "priority=1000" >> "$CELERY_BEAT_CFG"

# ### (2) WORKER Configuration for CELERY

[[ -f "$CELERY_WORKER_CFG" ]] && {
  echo "[WARN] <$CELERY_WORKER_CFG> exists, keeping a backup copy"
  mv -f "$CELERY_WORKER_CFG" "$CELERY_WORKER_CFG.bak"
}

echo '[program:tledb-worker]' > "$CELERY_WORKER_CFG"
echo "command=$(pwd)/.tledb/bin/celery -A $NAME worker -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler" >> "$CELERY_WORKER_CFG"
echo "directory=$(pwd)/tledb" >> "$CELERY_WORKER_CFG"
echo "user=$USER" >> "$CELERY_WORKER_CFG"
echo "numprocs=1" >> "$CELERY_WORKER_CFG"
echo "stdout_logfile=$(pwd)/logs/tledb-worker.log" >> "$CELERY_WORKER_CFG"
echo "stderr_logfile=$(pwd)/logs/tledb-worker.log" >> "$CELERY_WORKER_CFG"
echo "autostart=true" >> "$CELERY_WORKER_CFG"
echo "autorestart=true" >> "$CELERY_WORKER_CFG"
echo "startsecs=10" >> "$CELERY_WORKER_CFG"

# Need to wait for currently executing tasks to finish at shutdown.
# Increase this if you have very long running tasks.
echo "stopwaitsecs=600" >> "$CELERY_WORKER_CFG"
echo "stopasgroup=true" >> "$CELERY_WORKER_CFG"

# Set Celery priority higher than default (999)
# so, if rabbitmq is supervised, it will start first.
echo "priority=1000" >> "$CELERY_WORKER_CFG"
