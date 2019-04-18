FROM mysql:8

RUN echo "[mysqld]\nsecure-file-priv=""\ndefault_authentication_plugin=mysql_native_password\n" > /etc/mysql/conf.d/fuck.cnf

ENV MYSQL_ROOT_PASSWORD "fuck"

COPY messages /var/log/messages

COPY ./sql-scripts/ /docker-entrypoint-initdb.d/