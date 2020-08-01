Tutorial
========

.. meta::
    :description lang=en:
        Installing Grafana, PostgreSQL and InfluxDB with docker, creating animated maps
        with GeoLoop Panel plugin.
    :keywords: postgresql, influxdb, grafana, geoloop panel, worldmap panel, animated map

Quick Start
-----------

To start the application, install
`docker-compose <https://docs.docker.com/compose/install/>`__
on the host, clone this repo and run docker-compose from the
`docker <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/tree/master/docker>`__
directory.

.. code-block:: bash

    $ cd docker && docker-compose up -d

    Starting influx   ... done
    Starting postgres ... done
    Starting grafana  ... done

    $ docker ps

    CONTAINER ID        IMAGE                       PORTS                    NAMES
    e00c0bd0d4a5        grafana/grafana:latest      0.0.0.0:3000->3000/tcp   grafana
    2b33999d97b3        influxdb:latest             0.0.0.0:8086->8086/tcp   influx
    c4453cac69eb        postgres:latest             0.0.0.0:5433->5432/tcp   postgres

Three containers have been created and started. For the app services we expose the following ports:
3000 (grafana), 8086 (influx), 5432 (postgres). Note that we use ``HOST:CONTAINER`` mapping when specifying
postgres ports in docker-compose file. Inside a docker container, postgres is running on port ``5432``,
whereas the publicly exposed port outside the container is ``5433``.

.. code-block:: bash

    version: '3'

    services:
      postgres:
        ports:
          - "5433:5432"

Before we login to Grafana UI, we need to create PostgreSQL database. Note that we have already
created InfluxDB database specifying ``INFLUXDB_DB`` environment variable in docker-compose file.

To create postgres database we use
`psql <http://postgresguide.com/utilities/psql.html>`__, postgres terminal, inside the docker container. See
`Makefile <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/tree/master/docker/Makefile>`__
for more details.

.. code-block:: bash

    $ make -C docker/ postgres-create-db
    $ make -C docker/ postgres-init-schema

Now we can login to the Grafana web UI in browser (http://localhost:3000/grafana/) with the login ``admin`` and
password ``password`` and initialize data sources.

.. image:: /images/grafana_login.png
   :align: center
   :alt: Grafana login

Data Sources
------------

Before we create a dashboard, we need to add InfluxDB and PostgreSQL data sources. Follow
`this guide <https://grafana.com/docs/grafana/latest/features/datasources/add-a-data-source/>`__
to find out how to do this.

Here is the configuration parameters we use to add InfluxDB data source.

.. image:: /images/influx.png
   :align: center
   :alt: Configuration parameters used to add InfluxDB data source

And this is the configuration parameters we use to add PostgreSQL data source.

.. image:: /images/postgres.png
   :align: center
   :alt: Configuration parameters used to add PostgreSQL data source

The valid password for both data sources is ``password``. You can change the credentials in
`docker/.env <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/tree/master/docker/.env>`__
file before starting the service via ``docker-compose up``.

Populating the Database
-----------------------

To illustrate the process of building the animated map with GeoLoop Panel plugin, we will use time series data
tracking the number of people affected by COVID-19 worldwide, including confirmed cases of Coronavirus infection,
the number of people died while sick with Coronavirus, the number of people recovered from it.

We borrowed data from `"covid-19" dataset <https://github.com/datasets/covid-19>`__
and store it as csv files in `data <data/>`__ directory:

* `countries-aggregated.csv <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/tree/master/data/countries-aggregated.csv>`__ - cumulative cases (confirmed, recovered, deaths) across the globe.
* `us_confirmed.csv <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/tree/master/data/us_confirmed.csv>`__ - cumulative confirmed cases for US regions.
* `reference.csv <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/tree/master/data/reference.csv>`__ - regions metadata, location, names.

For writing this data to postgres tables we use ``COPY FROM`` command available via postgres console.
See `Makefile <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/tree/master/docker/Makefile>`__
for more details.

.. code-block:: bash

    $ make -C docker/ postgres-copy-data

After we have written data to the tables, we can login to terminal and view schema contents.

.. code-block:: bash

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

Now we calculate logarithm of the number of active cases and write it to InfluxDB database (measurement "covid").
We can also login to influx database from console and view the database contents.

.. code-block:: bash

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

Worldmap Panel
--------------

Let's visualize the number of confirmed cases across the US regions using Worldmap panel.
This panel is a tile map that can be overlaid with circles representing data points from a query.
It needs two sources of data: a location (latitude and longitude) and data that has link to a location.

The screenshot below shows query and configuration settings we used.

.. image:: /images/worldmap.png
   :align: center
   :alt: Configuring Worldmap Panel

And as the result we obtain the following map.

.. image:: /images/us.png
   :align: center
   :alt: Worldmap Panel example

See Worldmap Panel plugin `documentation <https://grafana.com/grafana/plugins/grafana-worldmap-panel>`__
for more details.

GeoLoop Panel
-------------

Now everything is ready to configure the GeoLoop panel and visualize Covid-19 growth rates.
Following `this tutorial <https://github.com/CitiLogics/citilogics-geoloop-panel/blob/master/README.md>`__,
we create a `GeoJSON <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/tree/master/data/countries.geojson>`__
with countries coordinates and wrap it up in a callback:

.. code-block:: bash

    geo({ "type": "FeatureCollection", ... });

To access geojson from grafana, we need to put it on a server somewhere. In this tutorial,
we will confine ourselves to serving the local directory where geojson is stored
(however, this approach is not recommended for production).

.. code-block:: bash

    $ make -C docker/ data-server

The GeoJSON URL: ``http://0.0.0.0:8000/countries.geojson``

A further step is to obtain a free `MapBox API Key <https://www.mapbox.com/developers/>`__,
the only thing is you need to create a mapbox account.

Here is the panel configuration settings.

.. image:: /images/geoloop.png
   :align: center
   :alt: Configuring GeoLoop Panel

And that's how it looks like.

.. image:: /images/preview.gif
   :align: center
   :alt: GeoLoop Panel
