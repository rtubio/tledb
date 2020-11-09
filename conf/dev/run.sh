#!/bin/bash

source 'conf/paths.conf'

docker build \
    --file "$DEV_DOCKERFILE"\
    --build-arg "DOCKER_ROOT=$DOCKER_ROOT"\
    --build-arg "PKGS_DEB=$DOCKER_DEBPKGS"\
    --build-arg "PKGS_PY=$DOCKER_PYPKGS"\
    --build-arg "USER=$DOCKER_USER"\
    --tag "$DEV_DOCKERNAME" .\
&& echo "「イメージ」完了しました" &&\
docker run\
    -p $DEV_DOCKERPORT:$DEV_DOCKERPORT\
    -v "$(pwd):$DOCKER_ROOT"\
    -it "$DEV_DOCKERNAME"\
    /bin/bash -c "su -l \"$DOCKER_USER\" && cd \"$DOCKER_ROOT\""
