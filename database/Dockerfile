FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD your_mysql_password

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306