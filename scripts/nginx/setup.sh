#!/bin/bash

nginx_conf () {
  filestr=$"
    sendfile        on;
    keepalive_timeout  65;

    ## Rewrite http to https
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name _;
        return 301 https://$NGINX_HOST$request_uri;
    }

    ## Use https
    server {
        add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; ";

        listen              443 ssl;
        server_name         $NGINX_DOMAIN;
        ssl_certificate     $NGINX_SSL_CERT;
        ssl_certificate_key $NGINX_SSL_KEY;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         HIGH:!aNULL:!MD5;

        location = /favicon.ico {
          access_log off; log_not_found off;
        }

        location /static/ {
            root $NGINX_STATIC;
        }

        location / {
            proxy_set_header Host               $NGINX_HOST;
            proxy_set_header X-Real-IP          $NGINX_REMOTE;
            proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host   $NGINX_HOST:$NGINX_PORT;
            proxy_set_header X-Forwarded-Server $NGHINX_HOST;
            proxy_set_header X-Forwarded-Port   $NGINX_PORT;
            proxy_set_header X-Forwarded-Proto  https;
            proxy_read_timeout 300s;
            proxy_pass http://$GU_HOST:$GU_PORT;
        }
    }
}
  "
  echo "$filestr" > $1
}

source 'config/scripts.config'
