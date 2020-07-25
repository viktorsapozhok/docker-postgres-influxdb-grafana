# docker-postgres-influxdb-grafana

This tutorial provides a quick guide of how to configure a dashboard environment 
from Grafana, Postgres and InfluxDB, create map overlays with Worldmap Panel plugin and 
build animated maps using GeoLoop Panel plugin.

To illustrate the process of building the animated maps with GeoLoop, 
we will use time series data tracking the number of people affected by COVID-19 worldwide, 
including confirmed cases of Coronavirus infection, the number of people died while 
sick with Coronavirus, and the number of people recovered from it.

The data is borrowed from [“covid-19” dataset](https://github.com/datasets/covid-19) 
and stored as csv files in [data](data/) directory.

[Read the tutorial](https://docker-postgres-influxdb-grafana.readthedocs.io/en/latest/tutorial.html) for more.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/source/images/dashboard.gif">
