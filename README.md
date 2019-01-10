# tledb
Database with the TLE's from NORAD, imported into a database and offered through a REST api.

# setup

The following script should guide you through the installation steps of the full stack:

    bash scripts/setup.sh

# running

Once installed, the service can be accessed directly through nginx+gunicorn (TBD) or by running the Django development server:

    python manage.py runserver
