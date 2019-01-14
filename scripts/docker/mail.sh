#!/bin/bash

create_mail_secrets () {
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


source 'config/scripts.config'

[[ -f "$MAIL_SECRETS" ]] && {
  echo '[WARN] MAIL secrets exists, skipping configuration'...
  exit 0
}

echo -n 'Please input the host for the mail account: '
read host
echo
echo -n 'Please input the port for the mail account: '
read port
echo
echo -n 'Please input the user for the mail account: '
read user
echo
echo -n 'Please input password for the mail account: '
read -s password
echo
echo -n 'Please input your password again:'
read -s password2
echo

[[ "$password" == "$password2" ]] && {

  echo 'Passwords match, create the secrets file...'
  create_mail_secrets "$MAIL_SECRETS" "$host" "$port" "$user" "$password"

} || {
  echo 'Passwords do not match, please execute again...'
  exit -1
}
