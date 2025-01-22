import logging
from time import sleep
from typing import Iterator
from urllib.error import HTTPError

from .source_data_model import RollCallVote, parse_roll_call_vote_from_url
from .settings import Settings


logger = logging.getLogger(__name__)


def create_house_url(base_url: str, year: int, roll_call_number: int):
    return f"{base_url}/{year}/roll{roll_call_number:03}.xml"


def scrape_single(settings: Settings, year: int, roll_call_number: int) -> RollCallVote:
    url = create_house_url(settings.house_url, year, roll_call_number)
    return parse_roll_call_vote_from_url(url)


def scrape_house_starting_at(
    settings: Settings, year: int, roll_call_number: int
) -> Iterator[RollCallVote]:

    # just used for logging
    num_votes_scraped = 0

    # This is set true when we should end scraping, rather than continue to the next year.
    # It prevents trying years beyond one plus the present year
    error_indicates_empty_year = True

    while True:
        try:
            # Get vote
            vote = scrape_single(settings, year, roll_call_number)
            yield vote

            # Reset if there is at least one vote in a year
            error_indicates_empty_year = False

            # Be polite
            sleep(settings.crawl_delay_seconds)

            # Increment counts
            roll_call_number += 1
            num_votes_scraped += 1
        except HTTPError as e:
            if e.status == 404:
                logger.info("Reached end of %d with a total of %d votes", year, num_votes_scraped)
                if error_indicates_empty_year:
                    logger.debug("Year %d did not have a first vote. Assuming this is the end of the data", year)
                    break
                else:
                    year += 1
                    roll_call_number = 1
                    num_votes_scraped = 0
                    error_indicates_empty_year = True
                    logger.debug("Will now scrape %d for first vote", year)
            else:
                logger.error(
                    "Unexpected response %d %s when trying to fetch house %d-%d",
                    e.status,
                    e.reason,
                    year,
                    roll_call_number,
                )
