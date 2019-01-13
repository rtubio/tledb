#!/bin/bash

# Small script-lib that provides a function to create a conf.d valid
# supervisor file

create_config() {

  echo "
[program:$2]
command=$4
directory=$3
user=$5
numprocs=1
stdout_logfile=/dev/fd/1
stdout_logfile_maxbytes=0
stderr_logfile=/dev/fd/2
stderr_logfile_maxbytes=0
redirect_stderr=true
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
stopasgroup=true
priority=1000
  " > $1

}
