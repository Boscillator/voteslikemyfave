import logging
import itertools
from pprint import pprint
from typing import Iterator

from .house import scrape_house
from .senate import scrape_senate
from .senate.member_list import fetch_member_list
from .settings import Settings
from .database import connect, insert_roll_calls_with_votes
from .bioguide import parse_json_to_dataclass

if __name__ == "__main__":
    settings = Settings.from_environs()

    # Configure logging
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Silence dubious neo4j notifications
    logging.getLogger('neo4j.notifications').setLevel(logging.WARN)

    # Connect to database
    driver = connect(settings)

    # Scrape and update database
    # scrape_senate(settings, driver)
    # scrape_house(settings, driver)

    pprint(parse_json_to_dataclass('/home/fred/Downloads/BioguideProfiles/S000033.json'))
