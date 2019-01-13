#!/bin/bash

# Simple script to create the docker file for the Django + Gunicorn app

#volumes:
# @tledb:
#  - .:$DCK_TARGET_DIR\

# @nginx:
#  - ../config/nginx-conf.d:$DCK_NGINX_CONFD
#  - static_volume:$DCK_NGINX_STATIC

config_compose() {
  filestr="
version: '2'
services:

  $DOCKER_APP_NAME:
    build:
      context: ../.
      dockerfile: $DOCKER_FILE_TLEDB
    networks:
      - nginx_network
      - db_network
    volumes:
      - static_volume:$DCK_STATIC
    depends_on:
      - mysqldb
      - rabbitmq

  nginx:
    build:
      context: ../.
      dockerfile: $DOCKER_FILE_NGINX
    ports:
      - 8000:80
    depends_on:
      - $DOCKER_APP_NAME
    volumes:
      - static_volume:$DCK_STATIC
    networks:
      - nginx_network

  rabbitmq:
    image: rabbitmq:3
    networks:
      - db_network

  mysqldb:
    image: mysql:5.7
    env_file:
      - $DOCKER_MYSQL_SECRETS
    networks:
      - db_network
    volumes:
      - db_vol:/var/lib/mysql

networks:
  nginx_network:
    driver: bridge
  db_network:
    driver: bridge

volumes:
  db_vol:
  static_volume:
"
  echo "$filestr" > $1
}

source 'config/scripts.config'
source 'config/docker.config'

config_compose "$DOCKER_COMPOSE"
