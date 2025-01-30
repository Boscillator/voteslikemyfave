import json
import glob
from .bioguide import BioguideEntry, PoliticianData
from pprint import pprint

if __name__ == '__main__':
  for p in glob.glob('/home/fred/Downloads/BioguideProfiles/*.json'):
    with open(p) as f:
      data = json.load(f)

      print(p)
      if 'data' in data:
        entry = BioguideEntry(**data)
      else:
        entry = BioguideEntry(data=PoliticianData(**data))

      print(entry.data.familyName);
