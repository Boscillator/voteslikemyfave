from __future__ import annotations
from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

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
