# Usage: make COMMAND
#
# Commands
#   help              Show help message.
#   create-database   Create postgres database.
#   init-schema       Initialize postgres schema.
#   service           Start up the application.
#   clean             Stop running application.
#   prune             Remove the containers.
#
include .env

PSQL = PGPASSWORD=$(POSTGRES_PASSWORD) \
	psql -h $(POSTGRES_HOST) -p $(POSTGRES_PORT) -U $(POSTGRES_USER)

help:
	@head -6 Makefile

create-database:
	$(PSQL) -c "CREATE DATABASE $(POSTGRES_DBNAME)"

init-schema:
	$(PSQL) -d $(POSTGRES_DBNAME) -f ../scripts/schema.sql

build:
	docker-compose up -d
	make create-database
	make init-schema

service:
	docker-compose up

stop:
	docker-compose down

clean:
	make stop
	docker system prune -af

clean-all:
	make clean
	docker volume prune

test:
	@echo $(POSTGRES_VOLUME)