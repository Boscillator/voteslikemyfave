from dataclasses import dataclass
from typing import Optional, Self
import os
import logging

PREFIX = "VOTE_SCRAPER"
DEFAULT_HOUSE_URL = "https://clerk.house.gov/evs"
DEFAULT_SENATE_MEMBER_URL = (
    "https://www.senate.gov/general/contact_information/senators_cfm.xml"
)
DEFAULT_SENATE_URL = "https://www.senate.gov/legislative/LIS/roll_call_votes"
DEFAULT_CRAWL_DELAY_SECONDS = 0.4
DEFAULT_NEO4J_URI = "neo4j://localhost:7687"
DEFAULT_NEO4J_USERNAME = "neo4j"
DEFAULT_RESUME_YEAR = 2025
DEFAULT_RESUME_CONGRESS = 119
DEFAULT_LOG_LEVEL = 'INFO'

@dataclass
class Settings:
    house_url: str
    crawl_delay_seconds: float
    senate_member_url: str
    senate_url: str
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: Optional[str]
    resume_year: int
    resume_congress: int
    log_level: int

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
            resume_year=int(os.environ.get(f'{PREFIX}_RESUME_YEAR', DEFAULT_RESUME_YEAR)),
            resume_congress=int(os.environ.get(f'{PREFIX}_RESUME_CONGRESS', DEFAULT_RESUME_CONGRESS)),
            log_level=getattr(logging, os.environ.get(f'{PREFIX}_LOG_LEVEL', DEFAULT_LOG_LEVEL))
        )
