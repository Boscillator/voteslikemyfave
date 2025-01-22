from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Iterator, Tuple, List
from datetime import datetime

import scraper.house as house

class Chamber(Enum):
  HOUSE_OF_REPS = 'house'
  SENATE = 'senate'

class Party(Enum):
  REPUBLICAN = 'R'
  DEMOCRAT = 'D'
  INDEPENDENT = 'I'

@dataclass
class Legislator:
  chamber: Chamber
  last_name: str
  party: Party
  state: str
  senate_id: Optional[str] = field(default=None)
  house_id: Optional[str] = field(default=None)
  first_name: Optional[str] = field(default=None)

  @property
  def full_name(self):
    return f"{self.last_name} ({self.party}-{self.state})"

@dataclass
class RollCall:
  chamber: Chamber
  congress: int
  session: int
  when: datetime
  question: str

@dataclass
class Vote:
  vote: str

@dataclass
class RollCallWithVotes:
  roll_call: RollCall
  votes: List[Tuple[Legislator, Vote]]

