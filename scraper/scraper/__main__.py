import logging
import itertools
from pprint import pprint
from typing import Iterator

from .house import scrape_house
from .senate import scrape_senate
from .senate.member_list import fetch_member_list
from .settings import Settings
from .database import connect, insert_roll_calls_with_votes

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
  settings = Settings.from_environs()
  driver = connect(settings)


  scrape_senate(settings, driver)
  scrape_house(settings, driver)

