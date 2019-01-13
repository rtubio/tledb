#!/bin/bash

# Small script that creates the configuration file for the NGINX docker

nginx_http () {
  echo "
upstream $DOCKER_APP_NAME {
    server $DOCKER_APP_NAME:$GU_PORT;
}

server {
    listen 80 deferred;

    location / {
      proxy_redirect off;
      proxy_pass http://$DOCKER_APP_NAME;
      #proxy_set_header Host \$host;
      #proxy_set_header X-Forwarded-Host \$server_name;
      #proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    #location /static {
    #  alias $DCK_NGINX_STATIC;
    #}

}
  " > $1
}


source 'config/scripts.config'
source 'config/docker.config'

[[ -d "$DOCKER_NGINX_CONFD" ]] || {
  echo "<$DOCKER_NGINX_CONFD> does not exist, creating..."
  mkdir -p "$DOCKER_NGINX_CONFD"
} && {
  echo "<$DOCKER_NGINX_CONFD> exists, skipping..."
}

nginx_http "$DOCKER_NGINX_CONF"
