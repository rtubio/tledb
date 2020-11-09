#!/bin/bash

create_django_config () {
  # Creates a file with the database configuration information for Django
  # $1 : string with the path to the file
  # $2 : string with the password

  filestr=$"
{
  \"ngin\": \"django.db.backends.mysql\",
  \"name\": \"$DBNAME\",
  \"user\": \"$DBUSER\",
  \"pass\": \"$2\",
  \"host\": \"$DBHOST\",
  \"port\": \"$DBPORT\"
}
  "

  echo "$filestr" > "$1"
}
