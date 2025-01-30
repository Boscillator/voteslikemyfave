import json
from .bioguide import BioguideEntry
from pprint import pprint

if __name__ == '__main__':
  with open('examples/sanders_bioguide.json') as f:
    data = json.load(f)

  bernie = BioguideEntry(**data)
  pprint(bernie.data.image) 
