#!/bin/bash

# Small script that creates the configuration file for the NGINX docker

nginx_http () {
  echo "

error_log /var/log/nginx/error.log debug;

upstream $DOCKER_APP_NAME {
    server $DOCKER_APP_NAME:$GU_PORT;
}

server {
    listen 80;

    location @proxy_to_app {
      proxy_redirect off;
      proxy_pass http://$DOCKER_APP_NAME;
      proxy_set_header Host \$http_host;
      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto \$scheme;
    }

    #location /static {
    #  alias $DCK_NGINX_STATIC;
    #}

}
  " > $1
}

nginx_full () {
  echo "

user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log debug;
pid        /var/run/nginx.pid;

events {
  worker_connections  1024;
}

http {
  include       /etc/nginx/mime.types;
  default_type  application/octet-stream;
  access_log /var/log/nginx/access.log combined;

  sendfile        on;
  #tcp_nopush     on;
  keepalive_timeout  65;

  upstream app {
    server $DOCKER_APP_NAME:$GU_PORT;
  }

  server {
    # use 'listen 80 deferred;' for Linux
    # use 'listen 80 accept_filter=httpready;' for FreeBSD
    listen 80;
    charset utf-8;
    root $DCK_WORK_DIR;

    # Handle noisy favicon.ico messages in nginx
     location = /favicon.ico {
        return 204;
        access_log     off;
        log_not_found  off;
    }

    location / {
        # checks for static file, if not found proxy to app
        try_files \$uri @proxy_to_app;
    }

    location @proxy_to_app {
        proxy_redirect     off;
        proxy_set_header   Host \$host;
        proxy_set_header   X-Real-IP \$remote_addr;
        proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host \$server_name;
        proxy_pass http://app;
    }
  }
}

  " > $1

}



source 'config/scripts.config'
source 'config/docker.config'

nginx_http "$DOCKER_NGINX_CONF"
nginx_full "$DOCKER_NGINX_CFG"
