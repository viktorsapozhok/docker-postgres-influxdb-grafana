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
	docker exec -i $(POSTGRES_CONTAINER) \
	psql -h $(POSTGRES_HOST) -p 5432 -U $(POSTGRES_USER)

help:
	@head -13 Makefile

postgres-console:
	PGPASSWORD=$(POSTGRES_PASSWORD) \
	docker exec -it $(POSTGRES_CONTAINER) \
	psql -h $(POSTGRES_HOST) -p 5432 -U $(POSTGRES_USER) -d $(POSTGRES_DBNAME)

postgres-create-db:
	$(PSQL) -c "CREATE DATABASE $(POSTGRES_DBNAME)"

postgres-init-schema:
	cat ../scripts/schema.sql | $(PSQL) -d $(POSTGRES_DBNAME)

postgres-copy-data:
	cat ../data/reference.csv | $(PSQL) -d $(POSTGRES_DBNAME) \
	-c "COPY covid.countries_ref FROM STDIN CSV HEADER"

	cat ../data/us_confirmed.csv | $(PSQL) -d $(POSTGRES_DBNAME) \
	-c "COPY covid.us_confirmed FROM STDIN CSV HEADER"

	cat ../data/countries-aggregated.csv | $(PSQL) -d $(POSTGRES_DBNAME) \
	-c "COPY covid.countries_aggregated FROM STDIN CSV HEADER"

postgres-delete-tables:
	cat ../scripts/delete_tables.sql | $(PSQL) -d $(POSTGRES_DBNAME)

influx-console:
	docker exec -it $(INFLUX_CONTAINER) influx -database '$(INFLUX_DBNAME)'

influx-copy-data:
	python ../scripts/write_points.py

build:
	docker-compose up -d
	make postgres-create-database
	make postgres-init-schema

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
