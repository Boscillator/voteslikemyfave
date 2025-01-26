from typing import Iterator
from datetime import datetime
from dataclasses import asdict
from .common import RollCallWithVotes, RollCall, Legislator, Vote
from .settings import Settings
from neo4j import GraphDatabase, Transaction
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


def insert_roll_call_vote(tx: Transaction, roll_call_vote: RollCall):
    properties = {
        "chamber": roll_call_vote.chamber.value,
        "congress": roll_call_vote.congress,
        "session": roll_call_vote.session,
        "number": roll_call_vote.number,
        "when": roll_call_vote.when,
        "question": roll_call_vote.question,
        "id": roll_call_vote.id,
    }

    query = "MERGE (rc: RollCall {id: $id}) ON CREATE SET rc += $properties"
    tx.run(query, properties=properties, id=roll_call_vote.id)


def insert_legislator(tx, legislator: Legislator):
    properties = {
        "chamber": legislator.chamber.value,
        "last_name": legislator.last_name,
        "party": legislator.party.value,
        "state": legislator.state,
        "id": legislator.id,
    }

    if legislator.senate_id is not None:
        properties["senate_id"] = legislator.senate_id

    if legislator.house_id is not None:
        properties["house_id"] = legislator.house_id

    if legislator.first_name is not None:
        properties["first_name"] = legislator.first_name

    query = "MERGE (l: Legislator {id: $id}) ON CREATE SET l += $properties"
    tx.run(query, properties=properties, id=legislator.id)


def create_relationship_for_legislator_to_vote(
    tx: Transaction, l: Legislator, roll_call: RollCall, vote: Vote
):
    query = """
        MATCH (l: Legislator {id: $legislator_id}), (r: RollCall {id: $roll_call_id})
        MERGE (l)-[v:VOTED_ON]->(r)
        ON CREATE SET v.vote = $vote
    """
    tx.run(query, legislator_id=l.id, roll_call_id=roll_call.id, vote=vote.vote)


def insert_roll_calls_with_votes(driver, roll_calls: Iterator[RollCallWithVotes]):
    def insert_data(tx, roll_call: RollCallWithVotes):
        insert_roll_call_vote(tx, roll_call.roll_call)

        for l, v in roll_call.votes:
            insert_legislator(tx, l)
            create_relationship_for_legislator_to_vote(tx, l, roll_call.roll_call, v)

    with driver.session() as session:
        for roll_call in roll_calls:
            session.write_transaction(insert_data, roll_call)
