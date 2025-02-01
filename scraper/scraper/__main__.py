import logging
import itertools
from pprint import pprint
from typing import Iterator

from .settings import Settings
from .database import connect
from .bioguide import insert_all_legislators
from .house import scrape_house

if __name__ == "__main__":
    settings = Settings.from_environs()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    driver = connect(settings)

    insert_all_legislators('/home/fred/Downloads/BioguideProfiles/*.json', driver)
    # scrape_house(settings, driver)

