import sqlite3
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def set_connection_psql():
    return create_engine("postgresql://data:dataviz@localhost:5432/carbolytics")


def get_tables(conn, used: int):

    data = sqlite3.connect("../data/crawl-data.sqlite")

    dns = pd.read_sql_query("SELECT * FROM dns_responses", data)
    cookies = pd.read_sql_query("SELECT * FROM javascript_cookies", data)
    sites = pd.read_sql_query("SELECT * FROM site_visits", data)

    # Custom index
    print("Reasigning ids...")
    uniq = pd.concat([dns['visit_id'], cookies['visit_id'],
                      sites['visit_id']]).unique()
    index = {}

    for ids in uniq:
        index[ids] = used + 1
        used += 1

    # Javascript_cookies table
    cookies[['is_http_only', 'is_host_only', 'is_session', 'is_secure']] = cookies[[
        'is_http_only', 'is_host_only', 'is_session', 'is_secure']].astype('bool')

    cookies['expiry'] = pd.to_datetime(cookies['expiry'], errors='coerce')
    cookies['time_stamp'] = pd.to_datetime(
        cookies['time_stamp'], errors='coerce')

    cookies['visit_id'] = cookies['visit_id'].map(index)

    cookies.drop(columns=['id', 'event_ordinal'], axis=1).to_sql(name='javascript_cookies', con=conn,
                                                                 if_exists='append', index=False)

    # DNS_respones table
    dns['visit_id'] = dns['visit_id'].map(index)

    dns.drop(['is_TRR', 'id'], axis=1).to_sql(name='dns_responses',
                                              con=conn, if_exists='append', index=False)

    # Site_visits table
    sites['visit_id'] = sites['visit_id'].map(index)

    sites.drop(columns=['site_rank']).to_sql(
        name='site_visits', con=conn, if_exists='append', index=False)

    return used


def last_site():

    conn = create_engine(
        "postgresql://data:dataviz@localhost:5432/carbolytics"
    )

    webs = pd.read_sql_query("SELECT site_url FROM site_visits", conn)

    webs['site_url'] = webs['site_url'].map(lambda x: x.lstrip('https://'))

    return set(webs['site_url'].unique())
