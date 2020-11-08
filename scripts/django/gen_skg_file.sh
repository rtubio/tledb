#!/bin/bash

create_secret() {
  # Creates the secrets file for Django with the given key
  # $1 : path to the secrets file to be created
  # $2 : secret key to be stored

  echo "
{
  \"secret_key\": \"$2\"
}
  " > $1

}
