#!/bin/bash


source 'config/scripts.config'
source "$gen_mail_file"

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
