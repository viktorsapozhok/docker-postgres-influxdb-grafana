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
	psql -h $(POSTGRES_HOST) -p $(POSTGRES_PORT_API) -U $(POSTGRES_USER)

help:
	@head -6 Makefile

create-database:
	$(PSQL) -c "CREATE DATABASE $(POSTGRES_DBNAME)"

init-schema:
	$(PSQL) -d $(POSTGRES_DBNAME) -f ../scripts/schema.sql

service:
	docker-compose up

clean:
	docker-compose down

prune:
	docker system prune -af

populate-data:
	python ../scripts/loaders.py

test:
	@echo $(POSTGRES_HOST)