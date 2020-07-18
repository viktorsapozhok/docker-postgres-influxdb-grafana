import os

from dotenv import load_dotenv
from influxdb import DataFrameClient
import numpy as np
import pandas as pd
from pgcom import Commuter

base_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/"
root_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))


def read_data(filename, rename_col=None):
    """Read data from csv.
    """
    df = pd.read_csv(base_url + filename)
    df.columns = map(str.lower, df.columns)
    if rename_col is not None:
        df.rename(columns=rename_col, inplace=True)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df


def get_conn_params(db='postgres'):
    """Return database connection parameters.
    """
    params = dict()
    for key in ['host', 'port', 'user', 'password', 'dbname']:
        params[key] = os.getenv(db.upper() + '_' + key.upper())
    if db == 'influx':
        params['username'] = params.pop('user')
        params['database'] = params.pop('dbname')
    return params


if __name__ == '__main__':
    # load environment variables from file
    load_dotenv(os.path.join(root_dir, 'docker', '.env'))

    # init postgres client
    conn_params = get_conn_params(db='postgres')
    commuter = Commuter(**conn_params)

    # init influx client
    conn_params = get_conn_params(db='influx')
    client = DataFrameClient(**conn_params)

    # read countries reference data
    rename_col = {'country_region': 'country', 'long_': 'lon'}
    df = read_data('reference.csv', rename_col=rename_col)
    commuter.copy_from(
        table_name='countries_ref',
        data=df,
        schema='covid',
        format_data=True,
        where='1=1')

    # read aggregated statistics by countries
    df = read_data('countries-aggregated.csv')
    # upload to postgres
    commuter.copy_from(
        table_name='countries_aggregated',
        data=df,
        schema='covid',
        format_data=True,
        where='1=1')

    # upload to influx
    df.set_index('date', inplace=True)
    df['active'] = df['confirmed'] - df['recovered']
    client.write_points(
        dataframe=df,
        measurement='active_cases',
        tag_columns=['country'],
        field_columns=['active'],
        protocol='line')

    df['active_scaled'] = np.log(1 + 0.0001 * df['active'])
    client.write_points(
        dataframe=df,
        measurement='active_scaled',
        tag_columns=['country'],
        field_columns=['active_scaled'],
        protocol='line')
