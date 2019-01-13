# tledb
Database with the TLE's from NORAD, imported and offered through a REST api.

The server is based on Django + Celery, where the latter timely fetches the
TLE files from Celestrak and updates the database. django-rest-framework is
used to provide a basic REST api for remote users.

# Setup

The following script should guide you through the installation steps of the
full stack, which mainly guides the process through a Docker composition:

  bash scripts/docker/setup.sh

Once the docker composition is running, the superuser can be created by
accessing the container directly:

  docker exec -it config_tledb_1 bash
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

The following parameter can be added to curl to pretty print the response from
the server's API:

    curl -H 'Accept: application/json; indent=4' ...
