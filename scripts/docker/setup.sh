#!/bin/bash

source 'config/scripts.config'

echo "1) Creating Dockerfile for Django+Gunicorn"
bash "$dockerfile_sh"

echo "2) Configuring the files for Django and the mySQL"
bash "$docker_mysql_sh"
bash "$docker_mail_sh"

echo "3) Composing containers"
bash "$docker_nginx_sh"
bash "$docker_compose_sh"

echo "4) Creating the composition"
docker-compose -f "$DOCKER_COMPOSE" build
docker-compose -f "$DOCKER_COMPOSE" up -d
