from typing import Iterator
from datetime import datetime
from dataclasses import asdict
from .settings import Settings
from neo4j import GraphDatabase, Driver
import logging

logger = logging.getLogger(__name__)


def connect(settings: Settings) -> Driver:
    """
    Create and return a Neo4j driver instance using the provided settings.

    Args:
        settings (Settings): The settings object containing Neo4j connection details.

    Returns:
        neo4j.Driver: An instance of the Neo4j driver.
    """
    logger.debug('Attempting to connect to neo4j at "%s"', settings.neo4j_uri)

    if settings.neo4j_password is None:
        logger.error("No password provided to database. Please set VOTE_SCRAPER_NEO4J_PASSWORD enviroment variable")
        raise ValueError("No database password set")

    try:
        driver = GraphDatabase.driver(
            settings.neo4j_uri, auth=(settings.neo4j_username, settings.neo4j_password)
        )
        logger.info("Connected to database")
        return driver
    except Exception as e:
        logger.error("Failed to initialized neo4j driver: %s", repr(e))
        raise
