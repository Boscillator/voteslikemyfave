from dataclasses import dataclass, field
from typing import Self
import os

PREFIX = "VOTE_SCRAPER"
DEFAULT_HOUSE_URL = "https://clerk.house.gov/evs"
DEFAULT_SENATE_MEMBER_URL = (
    "https://www.senate.gov/general/contact_information/senators_cfm.xml"
)
DEFAULT_SENATE_URL = "https://www.senate.gov/legislative/LIS/roll_call_votes"
DEFAULT_CRAWL_DELAY_SECONDS = 0.4
DEFAULT_NEO4J_URI = "neo4j://localhost:7687"
DEFAULT_NEO4J_USERNAME = "neo4j"


@dataclass
class Settings:
    house_url: str
    crawl_delay_seconds: float
    senate_member_url: str
    senate_url: str
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str

    @classmethod
    def from_environs(cls) -> Self:
        return cls(
            house_url=os.environ.get(f"{PREFIX}_HOUSE_URL", DEFAULT_HOUSE_URL),
            senate_member_url=os.environ.get(
                f"{PREFIX}_SENATE_MEMBER_URL", DEFAULT_SENATE_MEMBER_URL
            ),
            senate_url=os.environ.get(f"{PREFIX}_SENATE_URL", DEFAULT_SENATE_URL),
            crawl_delay_seconds=float(
                os.environ.get(
                    f"{PREFIX}_CRAWL_DELAY_SECONDS", DEFAULT_CRAWL_DELAY_SECONDS
                )
            ),
            neo4j_uri=os.environ.get(f"{PREFIX}_NEO4J_URI", DEFAULT_NEO4J_URI),
            neo4j_username=os.environ.get(
                f"{PREFIX}_NEO4J_USERNAME", DEFAULT_NEO4J_USERNAME
            ),
            neo4j_password=os.environ.get(f"{PREFIX}_NEO4J_PASSWORD"),
        )
