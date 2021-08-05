from tranco import Tranco
t = Tranco(cache=True, cache_dir='.tranco')


def get_list(date: str = '2021-01-01', webs: int = 1000):
    web_list = t.list(date=date)
    return web_list.top(webs)
