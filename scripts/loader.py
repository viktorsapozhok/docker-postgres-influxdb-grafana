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


def export_to_postgres(client, table_name, df):
    client.copy_from(table_name, df, format_data=True, where='1=1')


def export_to_influx(client, measurement, df, tag_columns, field_columns):
    client.write_points(
        df.set_index('date'), measurement,
        tag_columns=tag_columns, field_columns=field_columns, protocol='line')


if __name__ == '__main__':
    # load environment variables from file
    load_dotenv(os.path.join(root_dir, 'docker', '.env'))

    # init postgres client
    conn_params = get_conn_params(db='postgres')
    commuter = Commuter(**conn_params, schema='covid')

    # init influx client
    conn_params = get_conn_params(db='influx')
    client = DataFrameClient(**conn_params)

    # countries reference data
    df = read_data('reference.csv')
    export_to_postgres(commuter, 'countries_ref', df)

    # aggregated statistics by countries
    df = read_data('countries-aggregated.csv')
    export_to_postgres(commuter, 'countries_aggregated', df)

    # upload to influx
    df['active'] = df['confirmed'] - df['recovered'] - df['deaths']
    df['active_log'] = np.log(1 + 0.0001 * df['active'])
    export_to_influx(client, 'active', df, ['country'], ['active'])
    export_to_influx(client, 'active_log', df, ['country'], ['active_log'])

    # US confirmed/deaths statistics
    confirmed = read_data('us_confirmed.csv', rename_col={'case': 'confirmed'})
    deaths = read_data('us_deaths.csv', rename_col={'case': 'deaths'})
    df = confirmed[['uid', 'date', 'confirmed']].merge(
        deaths[['uid', 'date', 'deaths']], how='inner', on=['uid', 'date'])
    export_to_postgres(commuter, 'us_aggregated', df)
