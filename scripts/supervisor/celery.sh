#!/bin/bash

# TODO # check how to roll supervisor's logs!


create_config() {

  filestr=$"
[program:$1]
command=$3
directory=$4
user=$USER
numprocs=1
stdout_logfile=$5
stderr_logfile=$5
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
stopasgroup=true
priority=1000
  "

  echo "$filestr" > $2

}


source 'config/scripts.config'

[[ $( whoami ) == 'root' ]] || {
    echo 'Need to be <root>, exiting...' && exit -1
}

# ### (1) BEAT Configuration for CELERY
[[ -f "$CELERY_BEAT_CFG" ]] && {
  echo "[WARN] <$CELERY_BEAT_CFG> exists, keeping a backup copy"
  mv -f "$CELERY_BEAT_CFG" "$CELERY_BEAT_CFG.bak"
}

echo "[INFO] Creating config for '$CELERY_BEAT_APP'"
create_config\
  "$CELERY_BEAT_APP"\
  "$CELERY_BEAT_CFG"\
  "$CELERY_BIN -A $DJANGO_APP_NAME beat -l $LOGL --scheduler $CELERY_SCH"\
  "$CELERY_WD"\
  "$CELERY_BEAT_LOG"

# ### (2) WORKER Configuration for CELERY
[[ -f "$CELERY_WORKER_CFG" ]] && {
  echo "[WARN] <$CELERY_WORKER_CFG> exists, keeping a backup copy"
  mv -f "$CELERY_WORKER_CFG" "$CELERY_WORKER_CFG.bak"
}

echo "[INFO] Creating config for '$CELERY_WORKER_APP'"
create_config\
  "$CELERY_WORKER_APP"\
  "$CELERY_WORKER_CFG"\
  "$CELERY_BIN -A $DJANGO_APP_NAME worker -l $LOGL --scheduler $CELERY_SCH"\
  "$CELERY_WD"\
  "$CELERY_WORKER_LOG"

# ### (3) restart supervisor
echo "[INFO] Reloading <supervisor>"
sudo supervisorctl reread && sudo supervisorctl reload
