
# stack-back

![docs](https://readthedocs.org/projects/stack-back/badge/?version=latest)

Backup using [restic] for a docker-compose setup.

* [stack-back Documentation](https://stack-back.readthedocs.io)
* [stack-back on Github](https://github.com/lawndoc/stack-back)

Features:

* Backs up docker volumes or host binds
* Backs up postgres, mariadb, and mysql databases
* Notifications over mail/smtp or Discord webhooks

Please report issus on [github](https://github.com/lawndoc/stack-back/issues).

## Install

```bash
docker pull ghcr.io/lawndoc/stack-back
```

## Configuration (env vars)

Minimum configuration

```bash
RESTIC_REPOSITORY
RESTIC_PASSWORD
```

More config options can be found in the [documentation].

Restic backend specific env vars : https://restic.readthedocs.io/en/stable/040_backup.html#environment-variables

## Compose Example

We simply control what should be backed up by adding
labels to our containers. More details are covered
in the [documentation].

restic-backup.env

```bash
RESTIC_REPOSITORY=<whatever backend restic supports>
RESTIC_PASSWORD=hopefullyasecurepw
# snapshot prune rules
RESTIC_KEEP_DAILY=7
RESTIC_KEEP_WEEKLY=4
RESTIC_KEEP_MONTHLY=12
RESTIC_KEEP_YEARLY=3
# Cron schedule. Run every day at 1am
CRON_SCHEDULE="0 1 * * *"
```

docker-compose.yaml

```yaml
version: '3'
services:
  # The backup service
  backup:
    image: ghcr.io/lawndoc/stack-back:<version>
    env_file:
      - restic-backup.env
    volumes:
      # Communicate with docker to read backup tags
      - /var/run/docker.sock:/tmp/docker.sock:ro
      # Persistent restic cache (greatly speeds up all restic operations)
      - cache:/cache
  web:
    image: some_image
    labels:
      # Enables backup of the volumes below
      stack-back.volumes: true
    volumes:
      - media:/srv/media
      - /srv/files:/srv/files
  mariadb:
    image: mariadb:10
    labels:
      # Enables backup of this database
      stack-back.mariadb: true
    env_file:
      mariadb-credentials.env
    volumes:
      - mariadbdata:/var/lib/mysql
  mysql:
    image: mysql:5
    labels:
      # Enables backup of this database
      stack-back.mysql: true
    env_file:
      mysql-credentials.env
    volumes:
      - mysqldata:/var/lib/mysql

  postgres:
    image: postgres
    labels:
      # Enables backup of this database
      stack-back.postgres: true
    env_file:
      postgres-credentials.env
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  media:
  mysqldata:
  mariadbdata:
  pgdata:
  cache:
```

## The `rcb` command

Everything is controlled using the `rcb` command.
After configuring backup with labels and restarted
the affected services we can quickly view the
result using the `status` subcommand.

```bash
$ docker-compose run --rm backup rcb status
INFO: Status for compose project 'myproject'
INFO: Repository: '<restic repository>'
INFO: Backup currently running?: False
INFO: --------------- Detected Config ---------------
INFO: service: mysql
INFO:  - mysql (is_ready=True)
INFO: service: mariadb
INFO:  - mariadb (is_ready=True)
INFO: service: postgres
INFO:  - postgres (is_ready=True)
INFO: service: web
INFO:  - volume: media
INFO:  - volume: /srv/files
```

The `status` subcommand lists what will be backed up and
even pings the database services checking their availability.
The `restic` command can also be used directly in the container.

More `rcb` commands can be found in the [documentation].

## Running Tests

```bash
pip install -e ./src/
pip install -r src/tests/requirements.txt
tox
```

## Building Docs

```bash
pip install -r docs/requirements.txt
python src/setup.py build_sphinx
```

# Local dev setup

The git repository contains a simple local setup for development

```bash
# Create an overlay network to link the compose project and stack
docker network create --driver overlay --attachable global
# Start the compose project
docker-compose up -d
# Deploy the stack
docker stack deploy -c swarm-stack.yml test
```

In dev we should ideally start the backup container manually

```bash
docker-compose run --rm backup sh
# pip install the package in the container in editable mode to auto sync changes from host source
pip3 install -e .
```

Remember to enable swarm mode with `docker swarm init/join` and disable swarm
mode with `docker swarm leave --force` when needed in development (single node setup).

## Contributing

Contributions are welcome regardless of experience level.
Don't hesitate submitting issues, opening partial or completed pull requests.

[restic]: https://restic.net/
[documentation]: https://stack-back.readthedocs.io

---
This project is a fork of restic-compose-backup by [zetta.io](https://www.zetta.io)

[![Zetta.IO](https://raw.githubusercontent.com/lawndoc/stack-back/main/.github/logo.png)](https://www.zetta.io)
