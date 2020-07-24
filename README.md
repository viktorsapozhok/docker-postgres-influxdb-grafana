# docker-postgres-influxdb-grafana

This repo provides a quick guide of how to configure a dashboard environment from
[Grafana](https://github.com/grafana/grafana), Postgres and InfluxDB and build animated maps using 
[GeoLoop Panel](https://github.com/CitiLogics/citilogics-geoloop-panel) plugin.

## GeoLoop Panel Example

The following animation shows the total number of active Covid-19 cases reported in each country
at each point of time. Active cases = total confirmed - total recovered - total deaths.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/images/preview.gif">

## Quick Start

To start the application, install [docker-compose](https://docs.docker.com/compose/install/) 
on the host, clone this repo and run docker-compose from the [docker](/docker) directory.

```
$ cd docker && docker-compose up -d

Starting influx   ... done
Starting postgres ... done
Starting grafana  ... done

$ docker ps

CONTAINER ID        IMAGE                       PORTS                    NAMES
e00c0bd0d4a5        grafana/grafana:latest      0.0.0.0:3000->3000/tcp   grafana
2b33999d97b3        influxdb:latest             0.0.0.0:8086->8086/tcp   influx
c4453cac69eb        postgres:latest             0.0.0.0:5433->5432/tcp   postgres
```

Three containers have been created and started. For the app services we expose the following ports: 
3000 (grafana), 8086 (influx), 5432 (postgres). Note that we use `HOST:CONTAINER` mapping when specifying
postgres ports in docker-compose file. Inside a docker container, postgres is running on port `5432`, whereas the publicly exposed port
outside the container is `5433`. 

```
version: '3'

services:
  postgres:
    ports:
      - "5433:5432"
```

Before we login to Grafana UI, we need to create PostgreSQL database. Note that we have already created InfluxDB
database specifying `INFLUXDB_DB` environment variable in docker-compose file.

To create postgres database we use [psql](http://postgresguide.com/utilities/psql.html), postgres terminal, inside the docker
container. See [Makefile](/docker/Makefile) for more details.

```
$ make -C docker/ postgres-create-db
$ make -C docker/ postgres-init-schema
```

Now we can login to the Grafana web UI in browser (http://localhost:3000/grafana/) with the login `admin` and 
password `password` and initialize data sources.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/images/grafana_login.png" width="720">
   
## Data Sources

Before we create a dashboard, we need to add InfluxDB and PostgreSQL data sources.
Follow [this guide](https://grafana.com/docs/grafana/latest/features/datasources/add-a-data-source/) to find out
how to do this.

Here is the configuration parameters we use to add InfluxDB data source. 

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/images/influx.png" width="720">

This is the configuration parameters we use to add PostgreSQL data source.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/images/postgres.png" width="720">

The valid password for both data sources is `password`. You can change the credentials in [docker/.env](/docker/.env) file
before starting the service via `docker-compose up`.

## Populating the Database

To illustrate the process of building the animated map with GeoLoop Panel plugin, we will use time series data
tracking the number of people affected by COVID-19 worldwide, including confirmed cases of Coronavirus infection, 
the number of people died while sick with Coronavirus, the number of people recovered from it.

We borrowed data from ["covid-19" dataset](https://github.com/datasets/covid-19) and store it as csv files in [data](data/) directory: 

* [countries-aggregated.csv](data/countries-aggregated.csv) - cumulative cases (confirmed, recovered, deaths) across the globe.
* [us_confirmed.csv](data/us_confirmed.csv) - cumulative confirmed cases for US regions.
* [reference.csv](data/reference.csv) - regions metadata, location, names.

For writing this data to postgres tables we use `COPY FROM` command available via postgres console.
See [Makefile](/docker/Makefile) for more details.

```
$ make -C docker/ postgres-copy-data
```

After we have written data to the tables, we can login to terminal and view schema contents.

```
$ make -C docker/ postgres-console

psql (12.3 (Debian 12.3-1.pgdg100+1))
Type "help" for help.

grafana=# \dt+ covid.*
                            List of relations
 Schema |         Name         | Type  |  Owner   |  Size   | Description 
--------+----------------------+-------+----------+---------+-------------
 covid  | countries_aggregated | table | postgres | 1936 kB | 
 covid  | countries_ref        | table | postgres | 496 kB  | 
 covid  | us_confirmed         | table | postgres | 74 MB   | 
(3 rows)
```

Now we calculate logarithm of the number of active cases and write it to InfluxDB database (measurement "covid").
We can also login to influx database from console and view the database contents. 

```
$ make -C docker/ influx-console

Connected to http://localhost:8086 version 1.8.1
InfluxDB shell version: 1.8.1

> SHOW MEASUREMENTS
name: measurements
name
----
covid

> SHOW SERIES FROM covid LIMIT 5
key
---
covid,Country=Afghanistan
covid,Country=Albania
covid,Country=Algeria
covid,Country=Andorra
covid,Country=Angola
``` 

## Worldmap Panel

Let's visualize the number of confirmed cases across the US regions using Worldmap panel.
This panel is a tile map that can be overlaid with circles representing data points from a query.
It needs two sources of data: a location (latitude and longitude) and data that has link to a location.

The screenshot below shows query and configuration settings we used.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/images/worldmap.png" width="720">

And as the result we obtain the following map.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/images/us.png" width="720">

See Worldmap Panel plugin [documentation](https://grafana.com/grafana/plugins/grafana-worldmap-panel) for more details. 

## Geoloop Panel

Now everything is ready to configure the geoloop panel and visualize Covid-19 growth rates.
Following [this tutorial](https://github.com/CitiLogics/citilogics-geoloop-panel/blob/master/README.md), we
create a [GeoJSON](data/countries.geojson) with countries coordinates and wrap it up in a callback: `geo({ "type": "FeatureCollection", ... });`.

To access geojson from grafana, we need to put it on a server somewhere. In this tutorial, we will confine ourselves
to serving the local directory where geojson is stored (this approach is not recommended for production).

```
$ make -C docker/ data-server
``` 

The GeoJSON URL: `http://0.0.0.0:8000/countries.geojson`

A further step is to obtain a free [MapBox API Key](https://www.mapbox.com/developers/), the only thing is to create mapbox account.

Here is the panel configuration settings.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/images/geoloop.png" width="720">

And that's all, our dashboard now looks like this.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/images/dashboard.png" width="720">
