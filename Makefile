# Usage: make COMMAND
#
# Commands
#   help        Show help message.
#   service     Start up the application.
#
include .env

PSQL = PGPASSWORD=$(POSTGRES_PASSWORD) \
	psql -h $(POSTGRES_HOST) -p $(POSTGRES_PORT_API) -U $(POSTGRES_USER)

help:
	@head -6 Makefile

create-database:
	$(PSQL) -c "CREATE DATABASE $(POSTGRES_DBNAME)"

init-schema:
	$(PSQL) -d $(POSTGRES_DBNAME) -f scripts/schema.sql

service:
	docker-compose up

test:
	@echo $(POSTGRES_HOST)