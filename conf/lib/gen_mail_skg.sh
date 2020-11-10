#!/bin/bash

create_secret_mail () {
  # Creates a file with the mail secrets to be used for Django
  # $1 : path to the secrets file
  # $2 : host
  # $3 : port
  # $4 : user
  # $5 : pass

  echo "
  {
    \"back\": \"django.core.mail.backends.smtp.EmailBackend\",
    \"host\": \"$2\",
    \"port\": \"$3\",
    \"user\": \"$4\",
    \"pass\": \"$5\"
  }
  " > "$1"
}