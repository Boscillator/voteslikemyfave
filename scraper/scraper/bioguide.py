from __future__ import annotations
import glob
import json
import urllib.request
from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List, Optional
from datetime import datetime, date
from enum import Enum
from neo4j import Driver, Session, Transaction
import logging
import tempfile
import urllib
import zipfile

import scraper.models as models
from .settings import Settings

logger = logging.getLogger(__name__)

class Image(BaseModel):
    contentUrl: Optional[str] = None
    caption: Optional[str] = None
    name: Optional[str] = None

class Asset(BaseModel):
    name: str
    assetType: str
    contentUrl: str
    creditLine: Optional[str] = None
    usageRight: List[str] = []
    uploadDate: Optional[str] = None
    uploadDateISO: Optional[datetime] = None

class Party(BaseModel):
    name: str

class PartyAffiliation(BaseModel):
    party: Party

class Congress(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
    congressNumber: int
    congressType: str
    startDate: str
    endDate: Optional[str] = None

class Represents(BaseModel):
    regionType: str
    regionCode: str

class Note(BaseModel):
    type: str
    noteType: str
    content: str

class CongressAffiliation(BaseModel):
    congress: Optional[Congress] = None
    partyAffiliation: List[PartyAffiliation] = []
    caucusAffiliation: List[PartyAffiliation] = []
    represents: Optional[Represents] = None
    note: List[Note] = []
    departureReason: Optional[str] = None
    electionType: Optional[str] = None

class Job(BaseModel):
    name: str
    jobType: str

class JobPosition(BaseModel):
    job: Job
    congressAffiliation: CongressAffiliation
    startCirca: Optional[bool] = False
    endCirca: Optional[bool] = False

class CreativeWork(BaseModel):
    freeFormCitationText: Optional[str] = None

class ResearchRecordLocation(BaseModel):
    name: str
    addressLocality: Optional[str] = None
    addressRegion: Optional[str] = None

class ResearchRecord(BaseModel):
    name: Optional[str] = None
    recordType: List[str] = []
    recordLocation: ResearchRecordLocation
    description: Optional[str] = None

class RelatedTo(BaseModel):
    usCongressBioId: str

class Relationship(BaseModel):
    relationshipType: str
    relatedTo: RelatedTo

class NameHistory(BaseModel):
    familyName: Optional[str] = None
    middleName: Optional[str] = None
    duplicateName: Optional[bool] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    givenName: Optional[str] = None
    startCirca: Optional[bool] = None
    endCirca: Optional[bool] = None

class PoliticianData(BaseModel):
    usCongressBioId: str
    familyName: str
    middleName: Optional[str] = None
    unaccentedMiddleName: Optional[str] = None
    givenName: str
    unaccentedFamilyName: str
    unaccentedGivenName: str
    nickName: Optional[str] = None
    honorificPrefix: Optional[str] = None
    honorificSuffix: Optional[str] = None
    birthDate: Optional[str] = None
    birthCirca: Optional[bool] = None
    birthDateUnknown: Optional[bool] = None
    deathDate: Optional[str] = None
    deathCirca: Optional[bool] = None
    deathDateUnknown: Optional[bool] = None
    image: List[Image] = []
    profileText: str
    asset: List[Asset]
    jobPositions: List[JobPosition]
    creativeWork: List[CreativeWork]
    researchRecord: List[ResearchRecord]
    deleted: bool = False
    relationship: List[Relationship] = []
    nameHistory: List[NameHistory] = []

class BioguideEntry(BaseModel):
    data: PoliticianData

def insert_bioguide_entry(tx: Transaction, entry: BioguideEntry):
    legislator = models.Legislator(
        bioguide_id=entry.data.usCongressBioId,
        family_name=entry.data.familyName,
        given_name=entry.data.givenName,
        unaccented_family_name=entry.data.unaccentedFamilyName,
        unaccented_given_name=entry.data.unaccentedGivenName,
        profile_text=entry.data.profileText,
        middle_name=entry.data.middleName,
        unaccented_middle_name=entry.data.unaccentedMiddleName,
        nick_name=entry.data.nickName,
        honorific_prefix=entry.data.honorificPrefix,
        birth_date=entry.data.birthDate,
        birth_circa=entry.data.birthCirca,
        birth_date_unknown=entry.data.birthDateUnknown,
        death_date=entry.data.deathDate,
        death_date_unknown=entry.data.deathDateUnknown
    )

    query = """
        MERGE (l: Legislator {bioguide_id: $bioguide_id})
        ON CREATE SET
            l = $legislator
        ON MATCH SET l = $ legislator
    """

    tx.run(query, bioguide_id=legislator.bioguide_id, legislator=legislator.model_dump(exclude_none=True))

    for relation in entry.data.relationship:
        is_related_to = models.IsRelatedTo(relationship_type=relation.relationshipType)
        query = """
            MATCH (self: Legislator {bioguide_id: $bioguide_id})
            MERGE (relative: Legislator {bioguide_id: $relative_id})
            MERGE (self)-[r: IS_RELATED_TO]->(relative)
            ON CREATE SET r = $is_related_to
        """
        tx.run(query, bioguide_id=legislator.bioguide_id, relative_id=relation.relatedTo.usCongressBioId, is_related_to=is_related_to.model_dump(exclude_none=True))

    for job in entry.data.jobPositions:
        if job.congressAffiliation.congress is None:
            continue

        is_member_of_congress = models.IsMemberOfCongress(
            parties=[party.party.name for party in job.congressAffiliation.partyAffiliation]
        )
        congress = models.Congress(
            number=job.congressAffiliation.congress.congressNumber,
            start_date=job.congressAffiliation.congress.startDate,
            end_date=job.congressAffiliation.congress.endDate
        )
        query="""
            MATCH (self: Legislator {bioguide_id: $bioguide_id})
            MERGE (congress: Congress {number: $congress.number})
            ON CREATE
                SET congress = $congress
            MERGE (self)-[m: IS_MEMBER_OF_CONGRESS]->(congress)
            ON CREATE
                SET m = $membership
        """
        tx.run(query,
            bioguide_id=legislator.bioguide_id,
            congress=congress.model_dump(exclude_none=True),
            membership=is_member_of_congress.model_dump(exclude_none=True),
        )

        if job.congressAffiliation is not None and job.congressAffiliation.represents is not None:
            state = models.State(code=job.congressAffiliation.represents.regionCode)
            represents = models.Represents()
            query="""
                MATCH (self: Legislator {bioguide_id: $bioguide_id})
                MERGE (state: State {code: $state.code})
                ON CREATE
                    SET state = $state
                MERGE (self)-[r: REPRESENTS]->(state)
                ON CREATE
                    SET r = $represents
            """
            tx.run(query,
                bioguide_id=legislator.bioguide_id,
                state=state.model_dump(exclude_none=True),
                represents=represents.model_dump(exclude_none=True)
            )


        for party_affiliation in job.congressAffiliation.partyAffiliation:
           party = models.Party(
               name=party_affiliation.party.name,
               abbreviation=models.Party.name_to_abbreviation(party_affiliation.party.name)
           )

           is_member_of_party = models.IsMemberOfParty()

           query = """
                MATCH (self: Legislator {bioguide_id: $bioguide_id})
                MERGE (party: Party {name: $party.name})
                ON CREATE
                    SET party = $party
                MERGE (self)-[m: IS_MEMBER_OF_PARTY]->(party)
                ON CREATE
                    SET m = $membership
            """
           tx.run(query, bioguide_id=legislator.bioguide_id, party=party.model_dump(exclude_none=True), membership=is_member_of_party.model_dump(exclude_none=True))


def insert_bioguide_file(path: str, session: Session):
    with open(path) as f:
        data = json.load(f)

    if 'data' in data:
        entry = BioguideEntry(**data)
    else:
        entry = BioguideEntry(data=PoliticianData(**data))

    session.execute_write(insert_bioguide_entry, entry)
    logger.info ("Inserted %s %s into database", entry.data.givenName, entry.data.familyName)
    
def insert_all_legislators(glob_pattern: str, driver: Driver):
    files = glob.glob(glob_pattern)
    logger.debug("Found %d legislators to insert", len(files))
    with driver.session() as session:
        session.run("""CREATE CONSTRAINT legislator_bioguide_id_unique IF NOT EXISTS
                    FOR (l: Legislator)
                    REQUIRE l.bioguide_id IS UNIQUE
        """)
        session.run("""CREATE CONSTRAINT congress_number_unique IF NOT EXISTS
                    FOR (c: Congress)
                    REQUIRE c.number IS UNIQUE
        """)
        session.run("""CREATE CONSTRAINT party_name_unique IF NOT EXISTS
                    FOR (p: Party)
                    REQUIRE p.name IS UNIQUE
        """)
        session.run("""CREATE CONSTRAINT state_code_unique IF NOT EXISTS
                    FOR (s: State)
                    REQUIRE s.code IS UNIQUE
        """)

        for file in files:
            insert_bioguide_file(file, session)


    