import logging
from pprint import pprint

from .source_data_model import parse_roll_call_vote_from_url, RollCallVote

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
  data = parse_roll_call_vote_from_url("https://clerk.house.gov/evs/2025/roll002.xml")
  # pprint(data)