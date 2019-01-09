#!/bin/bash

# TODO # check how to roll supervisor's logs!

create_config() {

  echo "[program:$1]" > "$2"
  echo "command=$3" >> "$2"
  echo "directory=$4" >> "$2"
  echo "user=$USER" >> "$2"
  echo "numprocs=1" >> "$2"
  echo "stdout_logfile=$5" >> "$2"
  echo "stderr_logfile=$5" >> "$2"
  echo "autostart=true" >> "$2"
  echo "autorestart=true" >> "$2"
  echo "startsecs=10" >> "$2"
  echo "stopwaitsecs=600" >> "$2"
  echo "stopasgroup=true" >> "$2"
  echo "priority=1000" >> "$2"

}

NAME='tledb'
CELERY_BEAT_CFG='/etc/supervisor/conf.d/tledb-beat.conf'
CELERY_BEAT_LOG='/etc/supervisor/conf.d/tledb-beat.log'
CELERY_WORKER_CFG='/etc/supervisor/conf.d/tledb-worker.conf'
CELERY_WORKER_LOG='/etc/supervisor/conf.d/tledb-worker.log'

[[ $( whoami ) == 'root' ]] || {
    echo 'Need to be <root>, exiting...' && exit -1
}

# ### (1) BEAT Configuration for CELERY
[[ -f "$CELERY_BEAT_CFG" ]] && {
  echo "[WARN] <$CELERY_BEAT_CFG> exists, keeping a backup copy"
  mv -f "$CELERY_BEAT_CFG" "$CELERY_BEAT_CFG.bak"
} || {
  echo "[INFO] Creating config for 'tledb-beat'"
  create_config 'tledb-beat' "$CELERY_BEAT_CFG"\
    "$(pwd)/.tledb/bin/celery -A $NAME beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler"\
    "$(pwd)/tledb" "$(pwd)/logs/tledb-beat.log"
}

# ### (2) WORKER Configuration for CELERY
[[ -f "$CELERY_WORKER_CFG" ]] && {
  echo "[WARN] <$CELERY_WORKER_CFG> exists, keeping a backup copy"
  mv -f "$CELERY_WORKER_CFG" "$CELERY_WORKER_CFG.bak"
} || {
  echo "[INFO] Creating config for 'tledb-worker'"
  create_config 'tledb-worker' "$CELERY_WORKER_CFG"\
    "$(pwd)/.tledb/bin/celery -A $NAME worker -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler"\
    "$(pwd)/tledb" "$(pwd)/logs/tledb-worker.log"
}
