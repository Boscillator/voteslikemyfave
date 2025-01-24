from typing import Iterator
from datetime import datetime
from .common import RollCallWithVotes
from .settings import Settings
from neo4j import GraphDatabase
import logging

logger = logging.getLogger(__name__)


def connect(settings: Settings) -> GraphDatabase:
    """
    Create and return a Neo4j driver instance using the provided settings.

    Args:
        settings (Settings): The settings object containing Neo4j connection details.

    Returns:
        neo4j.Driver: An instance of the Neo4j driver.
    """
    logger.debug('Attempting to connect to neo4j at "%s"', settings.neo4j_uri)
    try:
        driver = GraphDatabase.driver(
            settings.neo4j_uri, auth=(settings.neo4j_username, settings.neo4j_password)
        )
        logger.info("Connected to database")
        return driver
    except Exception as e:
        logger.error("Failed to initialized neo4j driver: %s", repr(e))
        raise

def filter_non_null_properties(properties: dict) -> dict:
    """
    Filters out None values from a dictionary.

    Args:
        properties (dict): The dictionary to filter.

    Returns:
        dict: A new dictionary with None values removed.
    """
    return {k: v for k, v in properties.items() if v is not None}

def build_merge_query(label: str, properties: dict) -> str:
    """
    Builds a dynamic MERGE query for a given label and properties.

    Args:
        label (str): The label of the node.
        properties (dict): The properties to include in the query.

    Returns:
        str: A Cypher MERGE query string.
    """
    filtered_properties = filter_non_null_properties(properties)
    return f"MERGE ({label} {{ {', '.join(f'{k}: ${k}' for k in filtered_properties)} }})"

def insert_roll_calls_with_votes(driver, roll_calls: Iterator[RollCallWithVotes]):
    def insert_data(tx, roll_call: RollCallWithVotes):
        # Create RollCall node
        roll_call_properties = {
            "id": f"{roll_call.roll_call.chamber.value}-{roll_call.roll_call.congress}-{roll_call.roll_call.session}-{roll_call.roll_call.when.timestamp()}",
            "chamber": roll_call.roll_call.chamber.value,
            "congress": roll_call.roll_call.congress,
            "session": roll_call.roll_call.session,
            "when": roll_call.roll_call.when.isoformat(),
            "question": roll_call.roll_call.question,
        }
        roll_call_query = build_merge_query("rc:RollCall", roll_call_properties)
        tx.run(roll_call_query, **filter_non_null_properties(roll_call_properties))

        for legislator, vote in roll_call.votes:
            # Prepare Legislator properties
            legislator_properties = {
                "id": legislator.senate_id or legislator.house_id or f"{legislator.last_name}-{legislator.state}",
                "chamber": legislator.chamber.value,
                "last_name": legislator.last_name,
                "party": legislator.party.value,
                "state": legislator.state,
                "first_name": legislator.first_name,
                "senate_id": legislator.senate_id,
                "house_id": legislator.house_id,
            }
            legislator_query = build_merge_query("leg:Legislator", legislator_properties)
            tx.run(legislator_query, **filter_non_null_properties(legislator_properties))

            # Create Vote edge
            vote_query = (
                "MATCH (rc:RollCall {id: $roll_call_id}), (leg:Legislator {id: $legislator_id}) "
                "MERGE (leg)-[v:VOTED {vote: $vote}]->(rc)"
            )
            tx.run(
                vote_query,
                roll_call_id=roll_call_properties["id"],
                legislator_id=legislator_properties["id"],
                vote=vote.vote,
            )

    with driver.session() as session:
        for roll_call in roll_calls:
            session.write_transaction(insert_data, roll_call)

