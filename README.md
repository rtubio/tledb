# tledb
Database with the TLE's from NORAD, imported and offered through a REST api.

The server is based on Django + Celery, where the latter timely fetches the
TLE files from Celestrak and updates the database. django-rest-framework is
used to provide a basic REST api for remote users.

# Setup

The following script should guide you through the installation steps of the full stack:

    bash scripts/setup.sh

# Running

Once installed, the service can be accessed directly through nginx+gunicorn (TBD) or by running the Django development server:

    python manage.py runserver
