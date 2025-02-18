from dataclasses import dataclass, field
from itertools import islice
from pprint import pprint
from typing import List, Optional, Tuple, Iterator, no_type_check
from urllib.request import urlopen
from time import sleep
import xml.etree.ElementTree as ET
import logging
from datetime import datetime

from neo4j import Driver, Transaction

import scraper.models as models

from ..settings import Settings
from .member_list import MemberList, fetch_member_list

logger = logging.getLogger(__name__)


@dataclass
class Document:
    document_congress: int
    document_type: str
    document_number: str
    document_name: str
    document_title: str
    document_short_title: Optional[str]


@dataclass
class Amendment:
    amendment_number: Optional[str]
    amendment_to_amendment_number: Optional[str]
    amendment_to_amendment_to_amendment_number: Optional[str]
    amendment_to_document_number: Optional[str]
    amendment_to_document_short_title: Optional[str]
    amendment_purpose: Optional[str]


@dataclass
class Count:
    yeas: Optional[int]
    nays: Optional[int]
    present: Optional[int]
    absent: Optional[int]


@dataclass
class TieBreaker:
    by_whom: Optional[str]
    tie_breaker_vote: Optional[str]


@dataclass
class Member:
    member_full: str
    last_name: str
    first_name: str
    party: str
    state: str
    vote_cast: str
    lis_member_id: str


@dataclass
class RollCallVote:
    congress: int
    session: int
    congress_year: int
    vote_number: int
    vote_date: datetime
    modify_date: str
    vote_question_text: str
    vote_document_text: str
    vote_result_text: str
    question: str
    vote_title: str
    majority_requirement: str
    vote_result: str
    document: Document
    amendment: Amendment
    count: Count
    tie_breaker: TieBreaker
    members: List[Member]


@no_type_check # not going to type-check chat-gpt generated code
def parse_roll_call_vote(xml_string: str) -> RollCallVote:
    root = ET.fromstring(xml_string)

    def get_text(element, tag):
        return element.find(tag).text if element.find(tag) is not None else None

    document = Document(
        document_congress=int(get_text(root.find("document"), "document_congress")),
        document_type=get_text(root.find("document"), "document_type"),
        document_number=get_text(root.find("document"), "document_number"),
        document_name=get_text(root.find("document"), "document_name"),
        document_title=get_text(root.find("document"), "document_title"),
        document_short_title=get_text(root.find("document"), "document_short_title"),
    )

    amendment = Amendment(
        amendment_number=get_text(root.find("amendment"), "amendment_number"),
        amendment_to_amendment_number=get_text(
            root.find("amendment"), "amendment_to_amendment_number"
        ),
        amendment_to_amendment_to_amendment_number=get_text(
            root.find("amendment"), "amendment_to_amendment_to_amendment_number"
        ),
        amendment_to_document_number=get_text(
            root.find("amendment"), "amendment_to_document_number"
        ),
        amendment_to_document_short_title=get_text(
            root.find("amendment"), "amendment_to_document_short_title"
        ),
        amendment_purpose=get_text(root.find("amendment"), "amendment_purpose"),
    )

    yeas = get_text(root.find("count"), "yeas")
    nays = get_text(root.find("count"), "nays")
    present = get_text(root.find("count"), "present")
    absent = get_text(root.find("count"), "absent")

    count = Count(
        yeas=yeas and int(yeas),
        nays=nays and int(nays),
        present=present and int(present),
        absent=absent and int(absent),
    )

    tie_breaker = TieBreaker(
        by_whom=get_text(root.find("tie_breaker"), "by_whom"),
        tie_breaker_vote=get_text(root.find("tie_breaker"), "tie_breaker_vote"),
    )

    members = []
    for member in root.find("members").findall("member"):
        members.append(
            Member(
                member_full=get_text(member, "member_full"),
                last_name=get_text(member, "last_name"),
                first_name=get_text(member, "first_name"),
                party=get_text(member, "party"),
                state=get_text(member, "state"),
                vote_cast=get_text(member, "vote_cast"),
                lis_member_id=get_text(member, "lis_member_id"),
            )
        )

    return RollCallVote(
        congress=int(get_text(root, "congress")),
        session=int(get_text(root, "session")),
        congress_year=int(get_text(root, "congress_year")),
        vote_number=int(get_text(root, "vote_number")),
        vote_date=datetime.strptime(get_text(root, "vote_date"), "%B %d, %Y, %I:%M %p"),
        modify_date=get_text(root, "modify_date"),
        vote_question_text=get_text(root, "vote_question_text"),
        vote_document_text=get_text(root, "vote_document_text"),
        vote_result_text=get_text(root, "vote_result_text"),
        question=get_text(root, "question"),
        vote_title=get_text(root, "vote_title"),
        majority_requirement=get_text(root, "majority_requirement"),
        vote_result=get_text(root, "vote_result"),
        document=document,
        amendment=amendment,
        count=count,
        tie_breaker=tie_breaker,
        members=members,
    )


def _construct_senate_url(
    base_url: str, congress: int, session: int, vote_number: int
) -> str:
    return f"{base_url}/vote{congress}{session}/vote_{congress}_{session}_{vote_number:05}.xml"

class VoteNoteFoundException(Exception):
    pass

def scrape_single_senate_vote(
    settings: Settings, congress: int, session: int, vote_number: int
) -> RollCallVote:
    url = _construct_senate_url(settings.senate_url, congress, session, vote_number)
    with urlopen(url) as response:
        raw = response.read()
        if b'DOCTYPE html' in raw:
            # Despite Al-Gore having invented the internet, the senate does not know what a 404 error is
            # we detect the error page and raise an exception
            raise VoteNoteFoundException("Unable to find vote")

        results = parse_roll_call_vote(raw)
        return results

def scrape_senate_starting_at(settings: Settings, congress: int, session: int, vote_number: int) -> Iterator[RollCallVote]:
    error_indicates_empty = True
    num_votes = 0
    
    while True:
        try:
            logger.debug("Will attempt to scrape %d-%d-%d", congress, session, vote_number)
            result = scrape_single_senate_vote(settings, congress, session, vote_number)
            yield result
            error_indicates_empty = False
            vote_number += 1
            num_votes += 1
            sleep(settings.crawl_delay_seconds)
        except VoteNoteFoundException as e:
            if error_indicates_empty:
                # First element does not exist; stop scraping
                logger.info("First vote of the %dth congress, session %d was not found. Done! Total of %d votes", congress, session, num_votes)
                break
            else:
                # Try to move to next set of votes
                vote_number = 1
                error_indicates_empty = True
                if session == 1:
                    # Move to the second session from the first
                    session += 1
                    logger.debug("Moving to second session of the %dth congress", congress)
                else:
                    congress += 1
                    session = 1
                    logger.debug("Moving to the %dth congress, session 1", congress)

def find_resume_point_for_senate(settings: Settings, driver: Driver) -> Tuple[int,int,int]:
    records, summary, keys = driver.execute_query("""
    MATCH (rc: RollCall)
    WHERE rc.chamber = 'senate'
    ORDER BY
        rc.congress DESC
        , rc.session DESC
        , rc.number DESC
    LIMIT 1
    RETURN rc
    """)

    if len(records) == 0:
        return settings.resume_congress, 1, 1

    last_vote = records[0].data()['rc']
    return last_vote['congress'], last_vote['session'], last_vote['number'] + 1

def insert_single_vote(tx: Transaction, vote: RollCallVote):
    roll_call_vote = models.RollCall(
        chamber=models.Chamber.SENATE,
        congress=vote.congress,
        session=vote.session,
        number=vote.vote_number,
        when=vote.vote_date,
        question=vote.question
    )

    query = """
        MERGE (rc: RollCall {
            chamber: $rc.chamber,
            congress: $rc.congress,
            session: $rc.session,
            number: $rc.number
        })
        ON CREATE SET rc = $rc
        MERGE (c: Congress { number: $rc.congress })
        MERGE (rc)-[:DURING_CONGRESS]->(c)
        """
    tx.run(query, rc=roll_call_vote.model_dump(exclude_none=True))

    for vote_cast in vote.members:
        query = """
        MATCH (l: Legislator)
        WHERE l.unaccented_family_name = $family_name
        MATCH (l)-[:REPRESENTS]->(:State{ code: $state})
        , (l)-[:IS_MEMBER_OF_PARTY]->(:Party { abbreviation: $party })
        , (l)-[:IS_MEMBER_OF_CONGRESS]->(:Congress { number: $congress })
        LIMIT 1
        MATCH (rc: RollCall {chamber: $rc.chamber, congress: $rc.congress, session: $rc.session, number: $rc.number})
        MERGE (l)-[vote: VOTED_ON]->(rc)
        ON CREATE SET vote = $voted
        RETURN l.bioguide_id as bioguide_id
        """
        voted = models.VotedOn(vote=vote_cast.vote_cast)
        result = tx.run(query,
            family_name=vote_cast.last_name,
            party=vote_cast.party,
            state=vote_cast.state,
            congress=roll_call_vote.congress, 
            rc=roll_call_vote.model_dump(exclude_none=True),
            voted=voted.model_dump(exclude_none=True))

        row = result.single()

        if row is None:
            logger.error("Unable for find bioguide id for %s (%s-%s)", vote_cast.last_name, vote_cast.party, vote_cast.state)
            continue

        bioguide_id = row['bioguide_id']

        # update state
        query = """
            MATCH (l: Legislator { bioguide_id: $bioguide_id})
            MATCH (new_state: State { code: $state })
            MERGE (l)-[:CURRENTLY_REPRESENTS]->(new_state)
            WITH l, new_state
            MATCH (l)-[old_rep: CURRENTLY_REPRESENTS]->(old_state: State)
            WHERE old_state.code <> new_state.code
            DELETE old_rep
        """
        tx.run(query, bioguide_id = bioguide_id, state=vote_cast.state)


        # update party
        query = """
            MATCH (l: Legislator { bioguide_id: $bioguide_id})
            MATCH (new_party: Party { abbreviation: $party })
            MERGE (l)-[:CURRENTLY_MEMBER_OF]->(new_party)
            WITH l, new_party
            MATCH (l)-[old_membership: CURRENTLY_MEMBER_OF]->(old_party: State)
            WHERE old_party.abbreviation <> new_party.abbreviation
            DELETE old_membership
        """
        tx.run(query, bioguide_id = bioguide_id, party=vote_cast.party)


def insert_senate_votes(driver: Driver, votes: Iterator[RollCallVote]):
    with driver.session() as session:
        for rc_vote in votes:
            session.execute_write(insert_single_vote, rc_vote)


def scrape_senate(settings: Settings, driver: Driver):
    year, session, vote_number = find_resume_point_for_senate(settings, driver)
    votes = scrape_senate_starting_at(settings, year, session, vote_number)
    insert_senate_votes(driver, votes)
