#!/bin/bash

# Small script to configure the database and the user for the 'tledb' server


create_sql () {
  # Creates a file with the SQL commands to be executed
  # $1 : string with the path to the file where the SQL commands are stored
  # $2 : string with the password for the new user to be created

  filestr=$"
create user if not exists '$DBUSER'@'$DBHOST' identified by '$2';
create database if not exists $DBNAME character set $DBCHARSET;
grant all on $DBNAME.* to '$DBUSER'@'$DBHOST';
flush privileges;
set global sql_mode='STRICT_TRANS_TABLES';
  "

  echo "$filestr" > "$1"
}


source "config/scripts.config"
source "config/sql.config"
source "$django_db_sh"

echo -n 'Please input password for the new MySQL database user:'
read -s password
echo
echo -n 'Please input your password again:'
read -s password2
echo

[[ "$password" == "$password2" ]] && {
  echo 'Passwords match, proceeding with the setup of the database'
  create_sql "$sql_file" "$password"
  echo 'Please input your <root> password to access the MySQL console:'
  sudo mysql -u root -p < "$sql_file"
  echo 'Creating the MYSQL JSON configuration for Django'
  create_django_config "$MYSQL_SECRETS" "$password"
} || {
  echo 'Passwords do not match, please execute again...'
}
