import neo4j from 'neo4j-driver';

export const CURRENT_CONGRESS = parseInt(process.env.CURRENT_CONGRESS || '119');
export const BIOGUIDE_PHOTO_ROOT = process.env.BIOGUIDE_PHOTO_ROOT || 'https://bioguide.congress.gov/photo/';
const neo4j_uri = process.env.NEO4J_URI || 'neo4j://database:7687';
const neo4j_username = process.env.NEO4J_USER || 'neo4j';
const neo4j_password = process.env.NEO4J_PASSWORD!;

const driver = neo4j.driver(neo4j_uri, neo4j.auth.basic(neo4j_username, neo4j_password));

export type LegislatorSummary = {
  bioguide_id: string,
  given_name: string,
  family_name: string,
  state: string,
  party: string,
  image: string
};


export async function list_legislators_by_congress(congress:number): Promise<LegislatorSummary[]> {
  const query = `
    MATCH (l: Legislator)-[:VOTED_ON]-(:RollCall { congress: $congress})
    MATCH (l)-[:CURRENTLY_MEMBER_OF]->(p: Party)
    MATCH (l)-[:CURRENTLY_REPRESENTS]->(s: State)
    RETURN DISTINCT l.bioguide_id as bioguide_id
      , l.given_name as given_name
      , l.family_name as family_name
      , l.image as image
      , s.code as state
      , p.abbreviation as party
  `;

  const { records } = await driver.executeQuery(query, {congress});
  const results = records.map(r => r.toObject() as LegislatorSummary);
  return results;
}

export async function get_legislator_by_congress_name_and_state(congress: number, family_name: string, state: string): Promise<Legislator | undefined> {
  const query = `
    MATCH (l: Legislator { family_name: $family_name})
      , (l)-[:CURRENTLY_REPRESENTS]->(State { code: $state })
      , (l)-[:IS_MEMBER_OF_CONGRESS]->(:Congress { number: $congress })
    LIMIT 1
    RETURN l as legislator
  `;
  const { records } = await driver.executeQuery(query, {congress, family_name, state});
  const results = records.map(r => r.toObject().legislator.properties as Legislator)
  return results.at(0);
}
