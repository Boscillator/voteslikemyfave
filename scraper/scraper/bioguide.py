from dataclasses import dataclass
from pprint import pprint
from typing import List, Optional
import json

@dataclass
class Image:
    contentUrl: str
    caption: str
    name: str

@dataclass
class Asset:
    name: str
    assetType: str
    contentUrl: str
    creditLine: str
    associatedEntity: List[str]
    usageRight: List[str]
    uploadDate: str
    uploadDateISO: str

@dataclass
class Party:
    name: str

@dataclass
class Congress:
    name: str
    congressNumber: int
    congressType: str
    startDate: str
    endDate: Optional[str] = None

@dataclass
class CongressAffiliation:
    congress: Congress
    partyAffiliation: List[Party]
    caucusAffiliation: List[Party]
    represents: dict

@dataclass
class Job:
    name: str
    jobType: str

@dataclass
class JobPosition:
    job: Job
    congressAffiliation: CongressAffiliation
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    startCirca: Optional[bool] = False
    endCirca: Optional[bool] = False

@dataclass
class CreativeWork:
    freeFormCitationText: str
    name: Optional[str] = None

@dataclass
class RecordLocation:
    name: str
    location: dict
    parentRecordLocation: Optional[dict] = None

@dataclass
class ResearchRecord:
    name: str
    recordType: List[str]
    recordLocation: RecordLocation
    description: Optional[str] = None

@dataclass
class CongressPerson:
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
    profileText: str
    deleted: bool
    image: List[Image]
    relationship: List[str]
    asset: List[Asset]
    jobPositions: List[JobPosition]
    creativeWork: List[CreativeWork]
    researchRecord: List[ResearchRecord]

def parse_json_to_dataclass(file_path: str) -> CongressPerson:
    with open(file_path, 'r') as f:
        data = json.load(f)['data']
        pprint(data)
    
    data['image'] = [Image(**img) for img in data.get('image', [])]
    data['asset'] = [Asset(**asset) for asset in data.get('asset', [])]
    data['jobPositions'] = [
        JobPosition(
            job=Job(**jp['job']),
            congressAffiliation=CongressAffiliation(
                congress=Congress(**jp['congressAffiliation']['congress']),
                partyAffiliation=[Party(name=p['party']['name']) for p in jp['congressAffiliation'].get('partyAffiliation', [])],
                caucusAffiliation=[Party(name=p['party']['name']) for p in jp['congressAffiliation'].get('caucusAffiliation', [])],
                represents=jp['congressAffiliation'].get('represents', {})
            ),
            startDate=jp.get('startDate'),
            endDate=jp.get('endDate'),
            startCirca=jp.get('startCirca', False),
            endCirca=jp.get('endCirca', False)
        ) for jp in data.get('jobPositions', [])
    ]
    data['creativeWork'] = [CreativeWork(**cw) for cw in data.get('creativeWork', [])]
    data['researchRecord'] = [
        ResearchRecord(
            name=rr['name'],
            recordType=rr['recordType'],
            description=rr.get('description'),
            recordLocation=RecordLocation(**rr['recordLocation'])
        ) for rr in data.get('researchRecord', [])
    ]
    
    return CongressPerson(**data)