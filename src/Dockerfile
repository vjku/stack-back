FROM restic/restic:0.17.3

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk update && apk add \
    python3 \
    py3-pip \
    dcron \
    mariadb-client \
    postgresql-client \
    mariadb-connector-c-dev 

ADD . /restic-compose-backup
WORKDIR /restic-compose-backup
RUN pip install -U pip setuptools wheel --break-system-packages && \
    pip install -e . --break-system-packages
ENV XDG_CACHE_HOME=/cache

ENTRYPOINT []
CMD ["./entrypoint.sh"]
