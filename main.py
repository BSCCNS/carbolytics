from concurrent.futures import thread
from copy import copy
from typing import Tuple, List
from pathlib import Path
import os
import random
from insert import set_connection_psql, get_tables

# Due to OpenWPM implementation, has to be copied to it's dir
from openwpm.config import BrowserParams, ManagerParams, validate_crawl_configs, validate_browser_params
from openwpm.storage.sql_provider import SQLiteStorageProvider
from openwpm.task_manager import TaskManager
from openwpm.command_sequence import CommandSequence
from openwpm.commands.browser_commands import GetCommand
from webs import get_list


def configure_crawl(threads: int = 5, tp: str = 'always', data_dir: str = '../data/') -> Tuple[ManagerParams, List[BrowserParams]]:

    # Crawler configuration
    manager_params = ManagerParams(num_browsers=threads)

    browser_params = [BrowserParams(
        bot_mitigation=True, display_mode='headless', tp_cookies=tp, donottrack=True) for _ in range(threads)
    ]

    # Data to save
    for browser in browser_params:
        browser.cookie_instrument = True
        browser.navigation_instrument = True
        browser.dns_instrument = True

       # Accept cookies
        browser.tp_cookies = "always"

    # Config validation
    [validate_browser_params(p) for p in browser_params]
    validate_crawl_configs(manager_params, browser_params)

    # Watchdogs used for large scale crawler
    manager_params.memory_watchdog = True
    manager_params.process_watchdog = True

    # Save up some memory (cloud)
    manager_params.memory_watchdog = True

    return manager_params, browser_params


def run_crawler(manager_params: ManagerParams, browser_params: List[BrowserParams], sites: List[str], index: int):

    # Set up tasks
    with TaskManager(manager_params, browser_params, SQLiteStorageProvider(Path(f"../data/crawl-data.sqlite")), None) as manager:

        for site in sites:
            def callback(success: bool, val: str = site) -> None:
                print(  # Concurrency goes BRRRRR
                    f"CommandSequence for {val} ran {'successfully' if success else 'unsuccessfully'}")

            command_seq = CommandSequence(
                site, site_rank=index, callback=callback)

            # Start by visiting the page
            command_seq.append_command(
                GetCommand(url=site, sleep=3), timeout=60)

            # Run commands across all browsers (simple parallelization)
            manager.execute_command_sequence(command_seq)


if __name__ == "__main__":
    jobs = os.getenv("N_BROWSERS")
    date = os.getenv("DATE")
    n_webs = int(os.getenv("N_WEBS"))

    # PostgreSQL
    connection = set_connection_psql()

    print("Fetching data...")
    sites = ["https://" + x for x in get_list(date=date, webs=n_webs)]

    splits = [sites[x:x+7500] for x in range(0, len(sites), 7500)]

    print(
        f"Running with {jobs} browser(s) over {n_webs} web(s) [{len(splits)} batch(es)]")

    for index, split in enumerate(splits):

        print(f"\n\n\nStarting batch {index}...\n\n\n")
        random.seed(index)

        manager_params, browser_params = configure_crawl(
            threads=int(jobs))

        run_crawler(manager_params=manager_params,
                    browser_params=browser_params, sites=split, index=index)

        get_tables(connection)

        print("DONE\n\n\n\n\n")
