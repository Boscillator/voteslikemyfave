import logging
import itertools
from pprint import pprint
from typing import Iterator

from .house import scrape_house
from .senate import scrape_senate
from .senate.member_list import fetch_member_list
from .settings import Settings
from .database import connect, insert_roll_calls_with_votes

if __name__ == "__main__":
    settings = Settings.from_environs()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    driver = connect(settings)

    scrape_senate(settings, driver)
    scrape_house(settings, driver)
