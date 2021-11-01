from tranco import Tranco
import csv

t = Tranco(cache=True, cache_dir='.tranco')


def get_list(date: str = '2021-01-01', webs: int = 1000):
    web_list = t.list(date=date)
    return web_list.top(webs)

def read_list(path: str):
    with open('top-1m.csv', 'r') as csv_file:
        return [x[1] for x in csv.reader(csv_file)]