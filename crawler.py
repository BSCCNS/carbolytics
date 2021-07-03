from typing import Tuple, List
from pathlib import Path

from OpenWPM.openwpm.config import BrowserParams, ManagerParams, validate_crawl_configs
# from OpenWPM.openwpm.storage.sql_provider import SQLiteStorageProvider
# from OpenWPM.openwpm.task_manager import TaskManager


def configure_crawl(threads: int = 5, tp: str = 'always', data_dir: str = './data/') -> Tuple[ManagerParams, List[BrowserParams]]:

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

    # Config validation
    validate_crawl_configs(manager_params, browser_params)

    manager_params.data_directory = Path(data_dir)
    manager_params.log_path = Path(data_dir + 'openwpm.log')

    # Save up some memory (cloud)
    manager_params.memory_watchdog = True

    return manager_params, browser_params


def run_crawler(websites: str):

    # Get websites to crawler from file
    with open(websites, "r") as webs:
        sites = {line.strip() for line in webs}


if __name__ == "__main__":
    manager_params, browser_params = configure_crawl()

    run_crawler("sites.txt")
