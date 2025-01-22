from dataclasses import dataclass, field
from typing import Self
import os

PREFIX = "VOTE_SCRAPER"
DEFAULT_HOUSE_URL = "https://clerk.house.gov/evs"
DEFAULT_CRAWL_DELAY_SECONDS = 0.1


@dataclass
class Settings:
    house_url: str
    crawl_delay_seconds: int

    @classmethod
    def from_environs(cls) -> Self:
        return cls(
            house_url=os.environ.get(f"{PREFIX}_HOUSE_URL", DEFAULT_HOUSE_URL),
            crawl_delay_seconds=int(
                os.environ.get(
                    f"{PREFIX}_CRAWL_DELAY_SECONDS", DEFAULT_CRAWL_DELAY_SECONDS
                )
            ),
        )
