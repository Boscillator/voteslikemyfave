from typing import Optional
from pydantic import BaseModel
from datetime import date

class Legislator(BaseModel):
  bioguide_id: str
  family_name: str
  given_name: str
  unaccented_family_name: str
  unaccented_given_name: str
  profile_text: str
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
  start_date: date
  end_date: date

class CongressAffiliation(BaseModel):
  last_party: Optional[str]

class Party(BaseModel):
  name: str
  abbreviation: Optional[str]

class PartyAffiliation(BaseModel):
  pass

