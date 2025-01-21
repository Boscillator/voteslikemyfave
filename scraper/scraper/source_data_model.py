from dataclasses import dataclass, field
from typing import List, Optional, Dict
from urllib.request import urlopen
import logging
import xml.etree.ElementTree as ET
import datetime

logger = logging.getLogger(__name__)

@dataclass
class Legislator:
    name_id: str
    sort_field: str
    unaccented_name: str
    party: str
    state: str
    role: str

@dataclass
class RecordedVote:
    legislator: Legislator
    vote: str

@dataclass
class VoteMetadata:
    majority: str
    congress: int
    session: str
    chamber: str
    rollcall_num: int
    legis_num: str
    vote_question: str
    vote_type: str
    vote_result: str
    action_datetime: datetime.datetime
    vote_desc: Optional[str] = None

@dataclass
class RollCallVote:
    vote_metadata: VoteMetadata
    vote_data: List[RecordedVote] = field(default_factory=list)
    source_url: Optional[str] = field(default=None)

def parse_rollcall_vote(xml_doc: str) -> RollCallVote:
    root = ET.fromstring(xml_doc)

    # Parse vote-metadata
    metadata_elem = root.find("vote-metadata")

    # Parse action date and time
    action_datetime = parse_action_datetime(metadata_elem)

    vote_metadata = VoteMetadata(
        majority=metadata_elem.findtext("majority"),
        congress=int(metadata_elem.findtext("congress")),
        session=metadata_elem.findtext("session"),
        chamber=metadata_elem.findtext("chamber"),
        rollcall_num=int(metadata_elem.findtext("rollcall-num")),
        legis_num=metadata_elem.findtext("legis-num"),
        vote_question=metadata_elem.findtext("vote-question"),
        vote_type=metadata_elem.findtext("vote-type"),
        vote_result=metadata_elem.findtext("vote-result"),
        action_datetime=action_datetime,
        vote_desc=metadata_elem.findtext("vote-desc")
    )

    # Parse vote-data
    vote_data = []
    for recorded_vote_elem in root.find("vote-data").findall("recorded-vote"):
        legislator_elem = recorded_vote_elem.find("legislator")
        legislator = Legislator(
            name_id=legislator_elem.attrib.get("name-id"),
            sort_field=legislator_elem.attrib.get("sort-field"),
            unaccented_name=legislator_elem.attrib.get("unaccented-name"),
            party=legislator_elem.attrib.get("party"),
            state=legislator_elem.attrib.get("state"),
            role=legislator_elem.attrib.get("role")
        )
        vote = recorded_vote_elem.findtext("vote")
        vote_data.append(RecordedVote(legislator=legislator, vote=vote))

    # Combine all components into the main RollCallVote data class
    return RollCallVote(
        vote_metadata=vote_metadata,
        vote_data=vote_data
    )

def parse_action_datetime(metadata_elem) -> datetime.datetime:
    action_date_str = metadata_elem.findtext("action-date")
    action_time_str = metadata_elem.find("action-time").attrib.get("time-etz")
    action_datetime = None

    try:
        action_datetime = datetime.datetime.strptime(f"{action_date_str} {action_time_str}", "%d-%b-%Y %H:%M")
        logger.debug("Parsed action datetime: %s", action_datetime)
    except Exception as e:
        logger.error("Failed to parse action datetime: %s", e)
        raise
    return action_datetime

def parse_roll_call_vote_from_url(url: str) -> RollCallVote:
    logger.debug("Fetching roll call vote from %s", url)
    with urlopen(url) as response:
        logger.debug("%s returned %d %s", url, response.status, response.reason)
        roll_call = parse_rollcall_vote(response.read())
        roll_call.source_url = url
        logger.debug('Parsed roll call. chamber="%s" congress=%d session="%s" rollcall_num=%d action_datetime=%s',
                     roll_call.vote_metadata.chamber,
                     roll_call.vote_metadata.congress,
                     roll_call.vote_metadata.session,
                     roll_call.vote_metadata.rollcall_num,
                     roll_call.vote_metadata.action_datetime)
        return roll_call
