docker-postgres-influxdb-grafana
================================

.. meta::
    :description lang=en:
        Quick guide of how to configure a dashboard environment from Grafana,
        Postgres and InfluxDB, create map overlays with Worldmap Panel plugin and
        build animated maps using GeoLoop Panel plugin.
    :keywords: postgresql, influxdb, grafana, geoloop panel, worldmap panel, animated map

This tutorial provides a quick guide of how to configure a dashboard environment
from Grafana, Postgres and InfluxDB, create map overlays with Worldmap Panel plugin and
build animated maps using GeoLoop Panel plugin.

To illustrate the process of building the animated maps with GeoLoop,
we will use time series data tracking the number of people affected by COVID-19 worldwide,
including confirmed cases of Coronavirus infection, the number of people died while
sick with Coronavirus, and the number of people recovered from it.

The data is borrowed from `“covid-19” dataset <https://github.com/datasets/covid-19>`__
and stored as csv files in `data <data/>`__ directory.

.. image:: /images/dashboard.gif
   :align: center
   :alt: Grafana dashboard example used Worldmap and GeoLoop Panel plugins to visualie "covid-19" data

.. toctree::
   :maxdepth: 2

   tutorial

MIT License (see `LICENSE <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/blob/master/LICENSE>`_).
