#!/bin/bash

# Simple script to create the docker file for the Django + Gunicorn app

# NOTE: although it is not recommended, I am executing supervisor within this
# image and, therefore, violating its immutability since I need to execute
# apt-get.

# NOTE: I run update but not upgrade with apt-get since I do not want to break
# the packages.

# NOTE: supervisor configuration is not trivial and must follow this tutorial:
# https://advancedweb.hu/2018/07/03/supervisor_docker/
# 1) supervisor must run in the foreground (nodaemon = true)
# 2) supervisor's processes must log directly to the console (/dev/fd/1)

# NOTE: launching supervisor is now done from within a bash file to include
# migrating django's database
# CMD [\"/usr/bin/supervisord\", \"-c\", \"/etc/supervisor/supervisord.conf\"]


config_dockerfile() {

  echo "
FROM python:3.7.2-stretch
ENV PYTHONUNBUFFERED 1
EXPOSE $GU_PORT

RUN mkdir -p $DCK_TARGET_DIR
RUN mkdir -p $DCK_LOGS
RUN mkdir -p $DCK_SECRETS
RUN mkdir -p $DCK_NGINX_STATIC

WORKDIR $DCK_WORK_DIR

RUN apt-get update && apt-get -y install supervisor sudo
COPY config/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./.secrets ./.secrets
COPY ./config ./config
COPY ./scripts ./scripts
COPY ./tledb ./tledb

RUN bash \"$dck_supervisord_sh\"
RUN bash \"$docker_django_sh\"

RUN useradd -ms /bin/bash $DCK_USER
RUN chown $DCK_USER:$DCK_USER -R $DCK_TARGET_DIR

CMD [\"/bin/bash\", \"$dck_launcher_sh\"]
  " > $1

}


source 'config/scripts.config'
source 'config/docker.config'

config_dockerfile "$DOCKER_FILE_TLEDB"
