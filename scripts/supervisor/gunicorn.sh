#!/bin/bash

source 'config/scripts.config'
source 'scripts/supervisor/conf.sh'

[[ $( whoami ) == 'root' ]] || {
    echo 'Need to be <root>, exiting...' && exit -1
}

# ### (1) gunicorn Configuration for CELERY
[[ -f "$GU_CONF" ]] && {
  echo "[WARN] <$GU_CONF> exists, keeping a backup copy"
  mv -f "$GU_CONF" "$GU_CONF.bak"
}

echo "[INFO] Creating config for '$GU_APP'"
create_config "$GU_APP" "$GU_CONF" "$GU_COMMAND" "$GU_WD" "$GU_LOG"
