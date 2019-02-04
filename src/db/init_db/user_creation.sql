
#Create users
#db_admin
CREATE USER db_admin WITH PASSWORD 'dbAdmin123' CREATEDB;
#user_admin
CREATE USER user_admin WITH PASSWORD 'dbAdmin123';

#DB creation
CREATE DATABASE userdb WITH OWNER = 'user_admin';