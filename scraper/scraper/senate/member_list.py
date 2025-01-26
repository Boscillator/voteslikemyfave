from dataclasses import dataclass
from typing import Optional, Dict
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import logging
import unidecode

from ..settings import Settings


logger = logging.getLogger(__name__)

@dataclass
class Member:
    member_full: str
    last_name: str
    first_name: str
    party: str
    state: str
    address: str
    phone: str
    email: str
    website: str
    member_class: str
    bioguide_id: str
    leadership_position: Optional[str] = None


@dataclass
class MemberList:
    members: Dict[str, Member]
    last_updated: str


def parse_contact_information(xml_string: str) -> MemberList:
    root = ET.fromstring(xml_string)

    members = {}
    for member_elem in root.findall("member"):
        member = Member(
            member_full=member_elem.findtext("member_full", ""),
            last_name=member_elem.findtext("last_name", ""),
            first_name=member_elem.findtext("first_name", ""),
            party=member_elem.findtext("party", ""),
            state=member_elem.findtext("state", ""),
            address=member_elem.findtext("address", ""),
            phone=member_elem.findtext("phone", ""),
            email=member_elem.findtext("email", ""),
            website=member_elem.findtext("website", ""),
            member_class=member_elem.findtext("class", ""),
            bioguide_id=member_elem.findtext("bioguide_id", ""),
            leadership_position=member_elem.findtext("leadership_position"),
        )
        member_name_unaccented = unidecode.unidecode(member.member_full)
        members[member_name_unaccented] = member

    last_updated = root.findtext("last_updated", "")
    return MemberList(members=members, last_updated=last_updated)


def fetch_member_list(settings: Settings) -> MemberList:
  logger.debug("Fetching senate member contact information")
  with urlopen(settings.senate_member_url) as response:
    results = parse_contact_information(response.read())
    logger.info("Got %d senate member's contact info", len(results.members))
    return results
