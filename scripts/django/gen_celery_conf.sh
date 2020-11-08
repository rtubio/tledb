#!/bin/bash

create_celery_conf() {
  # Creates the configuration for Celery / RabittMQ
  # $1 : path to the secrets file to be created

  echo "
{
  \"broker\": \"amqp://localhost\",
  \"backend\": \"django-db\"
}
  " > $1

}
