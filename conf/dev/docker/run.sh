#!/bin/bash

source 'conf/paths.conf'

docker run\
    --publish $DOCKER_PORT:$DOCKER_PORT\
    --volume "$(pwd):$DOCKER_ROOT"\
    --name "$DOCKER_NAME" -it "$DOCKER_NAME"\
    $*
