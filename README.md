# tledb - application overview

![Django CI](https://github.com/rtubio/tledb/workflows/Django%20CI/badge.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/rtubio/tledb/badge.svg?branch=master)](https://coveralls.io/github/rtubio/tledb?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/77cd187ba2c5436f8cd02627f5dda2db)](https://app.codacy.com/gh/rtubio/tledb?utm_source=github.com&utm_medium=referral&utm_content=rtubio/tledb&utm_campaign=Badge_Grade)

Database with the TLE's from NORAD, imported and offered through a REST api:

* The server is based on Django + Celery, where the latter timely fetches the TLE files from Celestrak and updates the database.
* django-rest-framework is used to provide a basic REST api for remote users.
* A webhook is implemented, so that a given URL is called whenever the TLEs selected by the user are updated.

Docker is used to wire up the following components:

* tledb-django -- Django webserver executed using Gunicorn and running celery instances (beat and worker). Supervisor controls the execution of gunicorn and celery instances.
* tledb-nginx -- simple nginx container.
* tledb-rabbitmq -- rabbitmq server from Docker Hub.
* tledb-mysql -- mysql server from Docker Hub.

# Setup

The following script should guide you through the installation steps of the full stack, which mainly guides the process through a Docker composition:

  bash scripts/docker/setup.sh

Once the docker composition is running, the superuser can be created by accessing the container directly:

  docker exec -it tledb-django bash
  cd tledb && python manage.py createsuperuser

# Running

Once installed, the service can be accessed directly at:

  http://localhost:8000

Django admin is enabled and can be accessed as usual:

  http://localhost:8000/admin

# API

Available REST api can be explored by accessing the following url:

    http://localhost:8000/api

Currently, the following two calls are available:

    curl http://localhost:8000/api/tle
    curl http://localhost:8000/api/tle?identifier=WISE

The following parameter can be added to curl to pretty print the response from the server's API:

    curl -H 'Accept: application/json; indent=4' ...
