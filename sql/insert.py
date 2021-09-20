from distutils.log import error
import sqlite3
import pandas as pd
from sqlalchemy import create_engine


def set_connection_psql():
    return create_engine("postgresql://data:dataviz@localhost:5432/carbolytics")


def get_tables(conn):
    data = sqlite3.connect("../data/crawl-data.sqlite")

    # Task table
    pd.read_sql_query("SELECT * FROM task", data).to_sql(name='task',
                                                         con=conn, if_exists='append', index=False)

    # Crawl table
    pd.read_sql_query("SELECT * FROM crawl", data).to_sql(name='crawl',
                                                          con=conn, if_exists='append', index=False)

    # Javascript_cookies table
    cookies = pd.read_sql_query("SELECT * FROM javascript_cookies", data)

    cookies[['is_http_only', 'is_host_only', 'is_session', 'is_secure']] = cookies[[
        'is_http_only', 'is_host_only', 'is_session', 'is_secure']].astype('bool')

    cookies['expiry'] = pd.to_datetime(cookies['expiry'], errors='coerce')
    cookies['time_stamp'] = pd.to_datetime(
        cookies['time_stamp'], errors='coerce')

    cookies.to_sql(name='javascript_cookies', con=conn,
                   if_exists='append', index=False)

    # DNS_respones table
    pd.read_sql_query("SELECT * FROM dns_responses", data).drop('is_TRR', axis=1).to_sql(
        name='dns_responses', con=conn, if_exists='append', index=False)

    # Site_visits table
    pd.read_sql_query("SELECT * FROM site_visits", data).to_sql(
        name='site_visits', con=conn, if_exists='append', index=False)
