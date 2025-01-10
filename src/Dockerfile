FROM restic/restic:0.17.3

RUN apk update && apk add \
    python3 \
    py3-pip \
    dcron \
    mariadb-client \
    mariadb-connector-c-dev

RUN apk add postgresql-client --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main

ADD . /stack-back
WORKDIR /stack-back
RUN pip install -U pip setuptools wheel --break-system-packages && \
    pip install -e . --break-system-packages
ENV XDG_CACHE_HOME=/cache

ENTRYPOINT []
CMD ["./entrypoint.sh"]
