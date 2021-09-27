from distutils.log import error
import sqlite3
import pandas as pd
from sqlalchemy import create_engine


def set_connection_psql():
    return create_engine("postgresql://data:dataviz@localhost:5432/carbolytics")


def get_tables(conn):
    data = sqlite3.connect("../data/crawl-data.sqlite")

    dns = pd.read_sql_query("SELECT * FROM dns_responses", data)
    cookies = pd.read_sql_query("SELECT * FROM javascript_cookies", data)
    sites = pd.read_sql_query("SELECT * FROM site_visits", data)

    # Custom index
    index = {x[0]: hash(f"{x[0]}-{hash(x[1])}")
             for x in zip(dns['visit_id'], dns['hostname'])}

    dns['visit_id'] = dns['visit_id'].map(index)
    cookies['visit_id'] = cookies['visit_id'].map(index)
    sites['visit_id'] = sites['visit_id'].map(index)

    # Javascript_cookies table
    cookies[['is_http_only', 'is_host_only', 'is_session', 'is_secure']] = cookies[[
        'is_http_only', 'is_host_only', 'is_session', 'is_secure']].astype('bool')

    cookies['expiry'] = pd.to_datetime(cookies['expiry'], errors='coerce')
    cookies['time_stamp'] = pd.to_datetime(
        cookies['time_stamp'], errors='coerce')

    cookies.to_sql(name='javascript_cookies', con=conn,
                   if_exists='append', index=False)

    # DNS_respones table
    dns.drop('is_TRR', axis=1).to_sql(name='dns_responses',
                                      con=conn, if_exists='append', index=False)

    # Site_visits table
    sites.to_sql(
        name='site_visits', con=conn, if_exists='append', index=False)
