#!/bin/bash

source 'conf/paths.conf'

docker build \
    --file "$DEV_DOCKERFILE"\
    --build-arg "DOCKER_ROOT=$DOCKER_ROOT"\
    --build-arg "PKGS_DEB=$DOCKER_DEBPKGS"\
    --build-arg "PKGS_PY=$DOCKER_PYPKGS"\
    --build-arg "USER=$DOCKER_USER"\
    --build-arg "PORT=$DOCKER_PORT"\
    --tag "$DOCKER_NAME" . \
&& echo "「イメージ」完了しました"
