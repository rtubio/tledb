#!/bin/bash

DBNAME='testdb'

# https://dev.mysql.com/doc/refman/5.5/en/database-use.html
# https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sql-mode-strict
# https://stackoverflow.com/quesSET GLOBAL sql_mode='STRICT_TRANS_TABLES';tions/37319690/enable-the-strict-mode-in-mysql

# utf8 is necessary to avoid problems with certain libraries
CREATE DATABASE $DBNAME CHARACTER SET utf8;

SHOW DATABASES;
USE $DBNAME;
GRANT ALL ON $DBNAME.* TO $USER@'localhost';
SET GLOBAL sql_mode='STRICT_TRANS_TABLES';
quit
