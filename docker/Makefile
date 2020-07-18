# Usage: make COMMAND
#
# Commands
#   help              Show help message.
#   create-database   Create postgres database.
#   init-schema       Initialize postgres schema.
#   build             Build application.
#   service           Start up application.
#   data-server       Serve data directory.
#   stop              Stop running application.
#   clean             Stop app and remove containers.
#   clean-all         Remove app, remove containers and volumes.
#
include .env

PSQL = PGPASSWORD=$(POSTGRES_PASSWORD) \
	psql -h $(POSTGRES_HOST) -p $(POSTGRES_PORT) -U $(POSTGRES_USER)

help:
	@head -13 Makefile

create-database:
	$(PSQL) -c "CREATE DATABASE $(POSTGRES_DBNAME)"

init-schema:
	$(PSQL) -d $(POSTGRES_DBNAME) -f ../scripts/schema.sql

build:
	docker-compose up -d
	make create-database
	make init-schema

service:
	docker-compose up -d

data-server:
	python -m http.server --directory ../data/

stop:
	docker-compose down

clean:
	make stop
	docker system prune -af

clean-all:
	make clean
	docker volume prune
