# docker-postgres-influxdb-grafana

This repo provides a quick guide of how to configure a dashboard environment from
[Grafana](https://github.com/grafana/grafana), Postgres and InfluxDB, build map overlays
using Worldmap Panel plugin and animated maps with 
[GeoLoop Panel](https://github.com/CitiLogics/citilogics-geoloop-panel) plugin.

## GeoLoop Panel Example

The following animation shows the total number of active Covid-19 cases reported
in each country at each point of time (logarithmic scale).
Active cases = total confirmed - total recovered - total deaths.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/source/images/preview.gif">

## Worldmap Panel Example

The map below illustrates the total number of confirmed Covid-19 cases across US regions.

<img src="https://raw.githubusercontent.com/viktorsapozhok/docker-postgres-influxdb-grafana/master/docs/source/images/us.png" width="720">

Read the [tutorial](https://docker-postgres-influxdb-grafana.readthedocs.io/en/latest/tutorial.html) for more.
