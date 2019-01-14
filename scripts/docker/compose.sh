#!/bin/bash

# Simple script to create the docker file for the Django + Gunicorn app


config_compose() {
  filestr="
version: '2'
services:

  $DOCKER_APP_NAME:
    build:
      context: ../.
      dockerfile: $DOCKER_FILE_TLEDB
    restart: always
    container_name: $DOCKER_APP_NAME-django
    networks:
      - nginx_network
      - db_network
    ports:
      - 9000:9000
      - 9001:9001
    volumes:
      - static_volume:$DCK_STATIC
    depends_on:
      - mysqldb
      - rabbitmq

  nginx:
    build:
      context: ../.
      dockerfile: $DOCKER_FILE_NGINX
    restart: always
    container_name: $DOCKER_APP_NAME-nginx
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
    restart: always
    container_name: $DOCKER_APP_NAME-rabbitmq
    networks:
      - db_network

  mysqldb:
    image: mysql:5.7
    restart: always
    container_name: $DOCKER_APP_NAME-mysql
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
