#!/bin/bash

# Adapts a basic supervisor configuration for Docker.


source 'config/scripts.config'
source 'config/docker.config'
source 'scripts/docker/supervisor/conf.sh'

# ### (1) BEAT Configuration for Supervisor
echo "[INFO] Creating config for '$CELERY_BEAT_APP'"
create_config "$CELERY_BEAT_CFG" "$CELERY_BEAT_APP" "$DCK_CELERY_WD"\
  "celery -A $DJANGO_APP_NAME beat -l $LOGL --scheduler $CELERY_SCH"\
   "$DCK_USER"

# ### (2) WORKER Configuration for Supervisor
echo "[INFO] Creating config for '$CELERY_WORKER_APP'"
create_config "$CELERY_WORKER_CFG" "$CELERY_WORKER_APP" "$DCK_CELERY_WD"\
  "celery -A $DJANGO_APP_NAME worker -l $LOGL --scheduler $CELERY_SCH"\
  "$DCK_USER"

# ### (3) gunicorn configuration for Supervisor
echo "[INFO] Creating config for '$GU_APP'"
create_config "$GU_CONF" "$GU_APP" "$DCK_GU_WD" "$DCK_GU_COM" "$DCK_USER"

# ### (4) sets supervisord to start in the foreground
echo "[INFO] Patching up default <$SUPERVISOR_CONF>"
sedexpr='s/\[supervisord\]/\[supervisord\]\nnodaemon=true/g'
sed -i "$SUPERVISOR_CONF" -e "$sedexpr"
