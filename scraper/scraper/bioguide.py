from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class Image(BaseModel):
    contentUrl: HttpUrl
    caption: Optional[str]
    name: str

class Asset(BaseModel):
    name: str
    assetType: str
    contentUrl: HttpUrl
    creditLine: Optional[str]
    usageRight: List[str]
    uploadDate: str
    uploadDateISO: str

class PartyAffiliation(BaseModel):
    name: str

class Congress(BaseModel):
    name: str
    congressNumber: int
    congressType: str
    startDate: str
    endDate: Optional[str]

class Represents(BaseModel):
    regionType: str
    regionCode: str

class CongressAffiliation(BaseModel):
    congress: Congress
    partyAffiliation: List[PartyAffiliation]
    represents: Represents

class Job(BaseModel):
    name: str
    jobType: str

class JobPosition(BaseModel):
    job: Job
    congressAffiliation: CongressAffiliation
    startCirca: Optional[bool] = False
    endCirca: Optional[bool] = False

class CreativeWork(BaseModel):
    freeFormCitationText: str

class ResearchRecordLocation(BaseModel):
    name: str
    addressLocality: str
    addressRegion: str

class ResearchRecord(BaseModel):
    name: str
    recordType: List[str]
    recordLocation: ResearchRecordLocation
    description: Optional[str]

class PoliticianData(BaseModel):
    usCongressBioId: str
    familyName: str
    givenName: str
    unaccentedFamilyName: str
    unaccentedGivenName: str
    birthDate: str
    birthCirca: bool
    birthDateUnknown: bool
    deathCirca: bool
    deathDateUnknown: bool
    image: List[Image]
    profileText: str
    asset: List[Asset]
    jobPositions: List[JobPosition]
    creativeWork: List[CreativeWork]
    researchRecord: List[ResearchRecord]
    deleted: bool

class DataWrapper(BaseModel):
    data: PoliticianData
