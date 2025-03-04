from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime

class Legislator(BaseModel):
  bioguide_id: str
  family_name: str
  given_name: str
  unaccented_family_name: str
  unaccented_given_name: str
  profile_text: str
  image: Optional[str] = None
  middle_name: Optional[str] = None
  unaccented_middle_name: Optional[str] = None
  nick_name: Optional[str] = None
  honorific_prefix: Optional[str] = None
  honorific_suffix: Optional[str] = None
  birth_date: Optional[str] = None
  birth_circa: Optional[bool] = None
  birth_date_unknown: Optional[bool] = None
  death_date: Optional[str] = None
  death_circa: Optional[bool] = None
  death_date_unknown: Optional[bool] = None

class IsRelatedTo(BaseModel):
  relationship_type: str

class Congress(BaseModel):
  number: int
  start_date: Optional[date] = None
  end_date: Optional[date] = None

class IsMemberOfCongress(BaseModel):
  parties: List[str]

class Party(BaseModel):
  name: str
  abbreviation: Optional[str]

  @staticmethod
  def name_to_abbreviation(name: str) -> Optional[str]:
    match name:
      case 'Republican':
        return 'R'
      case 'Democrat':
        return 'D'
      case 'Independent':
        return 'I'
      case _:
        return None

class IsMemberOfParty(BaseModel):
  pass

class State(BaseModel):
  code: str

class Represents(BaseModel):
  pass

class Chamber(str, Enum):
  HOUSE_OF_REPS = 'house'
  SENATE = 'senate'

class RollCall(BaseModel):
  chamber: Chamber
  congress: int
  session: int
  number: int
  when: datetime
  question: str

class VotedOn(BaseModel):
  vote: str

