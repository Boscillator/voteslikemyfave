import logging
import itertools
from pprint import pprint
from typing import Iterator

from .house import scrape_house_starting_at, RollCallVote
from .senate import scrape_senate_starting_at
from .senate.member_list import fetch_member_list
from .settings import Settings
from .database import connect, insert_roll_calls_with_votes

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
  settings = Settings.from_environs()
  driver = connect(settings)

  # votes: Iterator[RollCallVote] = scrape_house_starting_at(settings, 2025, 19)
  # insert_roll_calls_with_votes(driver, votes)
  for v in scrape_senate_starting_at(settings, 119, 1, 18):
    pprint(v)

