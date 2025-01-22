import logging
import itertools
from pprint import pprint
from typing import Iterator

from .house import scrape_house_starting_at, RollCallVote
from .settings import Settings

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
  settings = Settings.from_environs()
  pprint(settings)

  votes: Iterator[RollCallVote] = scrape_house_starting_at(settings, 2025, 1)
  for v in votes:
    pprint(v.vote_metadata) 
