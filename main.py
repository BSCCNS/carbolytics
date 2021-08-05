from typing import Tuple, List
from pathlib import Path
import csv
import os

# Due to OpenWPM implementation, has to be copied to it's dir
from openwpm.config import BrowserParams, ManagerParams, validate_crawl_configs
from openwpm.storage.sql_provider import SQLiteStorageProvider
from openwpm.task_manager import TaskManager
from openwpm.command_sequence import CommandSequence
from openwpm.commands.browser_commands import GetCommand


def configure_crawl(threads: int = 5, tp: str = 'always', data_dir: str = '../data/') -> Tuple[ManagerParams, List[BrowserParams]]:

    # Crawler configuration
    manager_params = ManagerParams(num_browsers=threads)
    browser_params = [BrowserParams(
        bot_mitigation=True, display_mode='headless', tp_cookies=tp) for _ in range(threads)
    ]

    # Data to save
    for browser in browser_params:
        # HTTP Requests & Respostes
        browser.cookie_instrument = True
        # HTTP cookie changes ??
        browser.cookie_instrument = True
        # WebRequests callstack
        browser.callstack_instrument = True
        # DNS resolution
        browser.dns_instrument = True
        # JS Web API calls
        browser.js_instrument = True

        browser.profile_archive_dir = Path(data_dir)

    # Config validation
    validate_crawl_configs(manager_params, browser_params)

    manager_params.data_directory = Path(data_dir)
    manager_params.log_path = Path(data_dir + 'openwpm.log')

    # Watchdogs used for large scale crawler
    manager_params.memory_watchdog = True
    manager_params.process_watchdog = True

    # Save up some memory (cloud)
    manager_params.memory_watchdog = True

    return manager_params, browser_params


def run_crawler(websites: str, manager_params: ManagerParams, browser_params: List[BrowserParams]):

    # Get websites to crawler from file
    with open(websites) as data:
        sites = ["https://" + row[1] for row in csv.reader(data)]

        print(f"Total: {len(sites)}")

        # Set up tasks
        with TaskManager(manager_params, browser_params, SQLiteStorageProvider(Path("../data/crawl-data.sqlite")), None) as manager:

            for index, site in enumerate(sites):
                def callback(success: bool, val: str = site) -> None:
                    print(
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
    print(f"Running with {jobs} browser(s)")
    manager_params, browser_params = configure_crawl(
        threads=int(jobs))

    run_crawler(websites="top1M.csv",
                manager_params=manager_params, browser_params=browser_params)
