from dataclasses import dataclass, field
from pprint import pprint
from typing import List, Optional, Tuple, Iterator
from urllib.request import urlopen
from time import sleep
import xml.etree.ElementTree as ET
import logging
from datetime import datetime

import scraper.common as common

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

    def to_common(
        self, member_list: MemberList
    ) -> Tuple[common.Legislator, common.Vote]:
        try:
            member_info = member_list.members[self.member_full]
        except KeyError as e:
            logger.error('Unable to find "%s" in member list', self.member_full)
            raise

        legislator = common.Legislator(
            chamber=common.Chamber.SENATE,
            last_name=self.last_name,
            first_name=self.first_name,
            party=common.Party(self.party),
            state=self.state,
            bioguide_id=member_info.bioguide_id,
            senate_id=self.lis_member_id,
        )
        vote = common.Vote(vote=self.vote_cast)
        return (legislator, vote)

    @property
    def full_name(self):
        return f"{self.last_name} ({self.party}-{self.state})"


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

    def to_common(self, member_list: MemberList) -> common.RollCallWithVotes:
        roll_call = common.RollCall(
            chamber=common.Chamber.SENATE,
            congress=self.congress,
            session=self.session,
            number=self.vote_number,
            when=self.vote_date,
            question=self.question,
        )

        return common.RollCallWithVotes(
            roll_call=roll_call, votes=[member.to_common(member_list) for member in self.members]
        )


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
        raw: str= response.read()
        if b'DOCTYPE html' in raw:
            # Despite Al-Gore having invented the internet, the senate does not know what a 404 error is
            # we detect the error page and raise an exception
            raise VoteNoteFoundException("Unable to find vote")

        results = parse_roll_call_vote(raw)
        return results

def scrape_senate_starting_at(settings: Settings, congress: int, session: int, vote_number: int) -> Iterator[common.RollCallWithVotes]:
    member_list = fetch_member_list(settings)

    error_indicates_empty = True
    
    while True:
        try:
            logger.debug("Winn attempt to scrape %d-%d-%d", congress, session, vote_number)
            result = scrape_single_senate_vote(settings, congress, session, vote_number)
            yield result.to_common(member_list)
            error_indicates_empty = False
            vote_number += 1
            sleep(settings.crawl_delay_seconds)
        except VoteNoteFoundException as e:
            if error_indicates_empty:
                # First element does not exist; stop scraping
                logger.debug("First vote of the %dth congress, session %d was not found. Done!", congress, session)
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
