import os

from dotenv import load_dotenv
import pandas as pd
from pgcom import Commuter

base_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/"
root_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))


def read_data(filename, index=None, rename_col=None):
    """Read data from csv.
    """
    df = pd.read_csv(base_url + filename)
    df.columns = map(str.lower, df.columns)
    if rename_col is not None:
        df.rename(columns=rename_col, inplace=True)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    if index is not None:
        df.set_index(index, inplace=True)
    return df


def get_conn_params(db='POSTGRES'):
    """Return database connection parameters.
    """
    params = dict()
    for key in ['host', 'port', 'user', 'password', 'dbname']:
        params[key] = os.getenv(db + '_' + key.upper())
    return params


if __name__ == '__main__':
    # load environment variables from file
    load_dotenv(os.path.join(root_dir, 'docker', '.env'))

    # init postgres client
    conn_params = get_conn_params()
    commuter = Commuter(**conn_params)

    # read aggregated statistics by countries
    df = read_data('countries-aggregated.csv')
    # upload data to postgres
    commuter.copy_from(
        'countries_aggregated', df, schema='covid', format_data=True)

    # read countries reference data
    df = read_data('reference.csv', rename_col={'long_': 'lon'})
    commuter.copy_from('countries_ref', df, schema='covid', format_data=True)
