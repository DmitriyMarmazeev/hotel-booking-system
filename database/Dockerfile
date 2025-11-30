FROM postgres:15

COPY init-scripts/ /docker-entrypoint-initdb.d/

RUN chmod a+r /docker-entrypoint-initdb.d/*