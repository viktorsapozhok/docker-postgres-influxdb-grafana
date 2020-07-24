docker-postgres-influxdb-grafana
================================

This tutorial provides a quick guide of how to configure a dashboard environment
from Grafana, Postgres and InfluxDB, build map overlays using Worldmap Panel plugin and
animated maps using GeoLoop Panel plugin.

GeoLoop Panel Example
---------------------

The following animation shows the total number of active Covid-19 cases reported
in each country at each point of time (logarithmic scale).
Active cases = total confirmed - total recovered - total deaths.

.. image:: /images/preview.gif
   :align: center

Worldmap Panel Example
----------------------

The map below illustrates the total number of confirmed Covid-19 cases across US regions.

.. image:: /images/us.png
   :align: center

.. toctree::
   :maxdepth: 2

   tutorial

MIT License (see `LICENSE <https://github.com/viktorsapozhok/docker-postgres-influxdb-grafana/blob/master/LICENSE>`_).
