# docker-postgres-influxdb-grafana

This repo provides a quick guide of how to configure a dashboard environment from
[Grafana](https://github.com/grafana/grafana), Postgres and InfluxDB and build animated maps using 
[GeoLoop Panel](https://github.com/CitiLogics/citilogics-geoloop-panel) plugin.

<p>&nbsp;</p>

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/images/preview.gif">

**<small>Fig.1: Number of active covid-19 cases by countries.</small>**

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
3000 (grafana), 8086 (influx), 5432 (postgres). Note that we use `HOST:CONTAINER` mapping when specify
postgres ports in docker-compose file:

```
version: '3'

services:
  postgres:
    ports:
      - "5433:5432"
```

Inside a docker container, postgres is running on port `5432`, whereas the publicly exposed port
outside the container is `5433`. 
   
## Data Sources
