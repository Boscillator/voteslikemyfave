from pydantic import BaseModel

class Legislator(BaseModel):
  id: str
  family_name: str
  given_name: str
  unaccented_family_name: str
  unaccented_given_name: str

