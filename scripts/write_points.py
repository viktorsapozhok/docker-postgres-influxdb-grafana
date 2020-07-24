from configparser import ConfigParser
import os

from influxdb import DataFrameClient
import numpy as np
import pandas as pd

root_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))

# get connection parameters
config = ConfigParser()
with open(os.path.join(root_dir, 'docker', '.env')) as file:
    config.read_string('[top]\n' + file.read())
config = {s: dict(config.items(s)) for s in config.sections()}['top']

# init influx client
client = DataFrameClient(
    host=config['influx_host'], port=config['influx_port'],
    username=config['influx_user'], password=config['influx_password'],
    database=config['influx_dbname'])

# read data
df = pd.read_csv(os.path.join(root_dir, 'data', 'countries-aggregated.csv'))
df['date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', utc=True)
df['active'] = df['Confirmed'] - df['Recovered'] - df['Deaths']
df['active_log'] = np.log(1 + 0.0001 * df['active'])

# import to influx
client.write_points(
    dataframe=df.set_index('date'), measurement='covid',
    tag_columns=['Country'], field_columns=['active_log'], protocol='line')
