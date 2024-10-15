FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=project

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306
