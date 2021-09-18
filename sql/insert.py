import sqlite3
import pandas as pd
from sqlalchemy import create_engine


def set_connection_psql():
    return create_engine("postgresql://data:dataviz@localhost:5432/carbolytics")


def get_tables(conn):
    con = sqlite3.connect("../data/crawl-data.sqlite")

    pd.read_sql_query("SELECT * FROM task", con).to_sql(name='task',
                                                        con=conn, if_exists='append', index=False)

    pd.read_sql_query("SELECT * FROM crawl", con).to_sql(name='crawl',
                                                         con=conn, if_exists='append', index=False)

    pd.read_sql_query("SELECT * FROM dns_responses", con).drop('is_TRR', axis=1).to_sql(
        name='dns_responses', con=conn, if_exists='append', index=False)

    pd.read_sql_query("SELECT * FROM javascript_cookies", con).to_sql(
        name='javascript_cookies', con=conn, if_exists='append', index=False)

    pd.read_sql_query("SELECT * FROM site_visits", con).to_sql(
        name='site_vists', con=conn, if_exists='append', index=False)
