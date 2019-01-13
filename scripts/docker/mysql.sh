#!/bin/bash

# Script to generate the secrets for the Dockerized MYSQL server and for Django
# Both secret files need to have the same information


create_docker_envfile () {
  # Creates a file with the same secrets. to be used for Docker

  echo "
MYSQL_ROOT_PASSWORD=$2
MYSQL_DATABASE=$DBNAME
MYSQL_USER=$DBUSER
MYSQL_PASSWORD=$2
  " > "$1"
}

# ### MAIN

source 'config/scripts.config'
source 'config/docker.config'
source 'config/sql.config'
source "$django_db_sh"

[[ -f "$DOCKER_MYSQL_SECRETS" ]] && [[ -f "$MYSQL_SECRETS" ]] && {
  echo '[WARN] Secret files exists, aborting password configuration'...
  exit 0
}

echo -n 'Please input password for the new MySQL database user:'
read -s password
echo
echo -n 'Please input your password again:'
read -s password2
echo

[[ "$password" == "$password2" ]] && {

  echo 'Passwords match, proceeding with the setup of the database'
  echo '>> Creating configuration for dockerized MySQL (envfile)'
  create_docker_envfile "$DOCKER_MYSQL_SECRETS" "$password"

  DBHOST="$DCK_DBHOST"
  echo ">> Creating the MYSQL for Django: <$DBHOST>"
  create_django_config "$MYSQL_SECRETS" "$password"

} || {
  echo 'Passwords do not match, please execute again...'
}
