#!/bin/bash

sudo service mysql stop
sudo mysqld_safe --skip-grant-tables &
mysql -uroot

use mysql;
update user set authentication_string=PASSWORD("XXXX") where User='root';
flush privileges;
quit

sudo service mysql stop
sudo service mysql start

# mysql -u root -p <<<< this should permit the loging with the new password
