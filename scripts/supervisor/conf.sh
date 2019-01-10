#!/bin/bash

# Small script-lib that provides a function to create a conf.d valid
# supervisor file

create_config() {

  filestr=$"
[program:$1]
command=$3
directory=$4
user=$USER
numprocs=1
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_logfile=$5
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
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
