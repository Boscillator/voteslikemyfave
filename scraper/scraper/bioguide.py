from __future__ import annotations
from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List, Optional
from datetime import datetime
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
    name: str
    congressNumber: int
    congressType: str
    startDate: str
    endDate: Optional[str] = None

class Represents(BaseModel):
    regionType: str
    regionCode: str

class CongressAffiliation(BaseModel):
    congress: Optional[Congress] = None
    partyAffiliation: List[PartyAffiliation] = []
    represents: Optional[Represents] = None

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
    class RelationshipType(str, Enum):
        FATHER_IN_LAW = 'father-in-law'
        SON = 'son'
        FATHER = 'father'
        GRANDFATHER = 'grandfather'
        GREAT_GRANDFATHER = 'great-grandfather'
        UNCLE = 'uncle'
        HALF_BROTHER = 'half brother'
        COUSIN = 'cousin'
        BROTHER = 'brother'
        DAUGHTER_IN_LAW = 'daughter-in-law'
        WIFE = 'wife'
        RELATIVE = 'relative'
        NEPHEW = 'nephew'
        GRANDSON = 'grandson'
        GREAT_GREAT_GREAT_GRANDFATHER = 'great-great-great-grandfather'
        GRAND_UNCLE = 'granduncle'
        GREAT_GRANDSON = 'great-grandson'
        GREAT_GREAT_GREAT_GRANDDAUGHTER = 'great-great-great-granddaughter'
        GREAT_GREAT_GRANDFATHER = 'great-great-grandfather'
        GRANDNEPHEW = 'grandnephew'
        HUSBAND = 'husband'
        GREAT_UNCLE = 'great-uncle'
        GREAT_GREAT_GRANDSON = 'great-great-grandson'
        GREAT_GREAT_GREAT_GRANDNEPHEW = 'great-great-great-grandnephew'
        GREAT_GREAT_GRANDNEPHEW = 'great-great-grandnephew'
        SISTER_IN_LAW = 'sister-in-law'
        MOTHER = 'mother'
        SON_IN_LAW = 'son-in-law'
        SISTER = 'sister'
        BROTHER_IN_LAW = 'brother-in-law'
        GREAT_GREAT_GREAT_GRANDSON = 'great-great-great-grandson'
        GREAT_GRANDUNCLE = 'great-granduncle'
        GREAT_GREAT_UNCLE = 'great-great-uncle'
        SECOND_COUSIN = 'second cousin'
        DAUGHTER = 'daughter'
        GREAT_GREAT_GRANDUNCLE = 'great-great-granduncle'
        GREAT_GREAT_GREAT_UNCLE = 'great-great-great-uncle'
        GRANDDAUGHTER = 'granddaughter'
        GREAT_GREAT_GREAT_NEPHEW = 'great-great-great-nephew'
        STEP_GREAT_GRANDSON = 'step-great-grandson'
        GREAT_GRANDNEPHEW = 'great-grandnephew'
        GREAT_GREAT_GREAT_GRANDUNCLE = 'great-great-great-granduncle'
        GREAT_NEPHEW = 'great-nephew'
        STEP_GRANDFATHER = 'step-grandfather'
        STEPFATHER = 'stepfather'
        GREAT_GREAT_GREAT_GREAT_GRANDUNCLE = 'great-great-great-great-granduncle'
        STEPMOTHER = 'stepmother'
        FIRST_COUSIN_ONCE_REMOVED = 'first cousin once removed'
        GREAT_GREAT_NEPHEW = 'great-great-nephew'
        GRANDMOTHER = 'grandmother'

    relationshipType: RelationshipType
    relatedTo: RelatedTo

class PoliticianData(BaseModel):
    model_config = ConfigDict(extra='forbid')

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

class BioguideEntry(BaseModel):
    data: PoliticianData
