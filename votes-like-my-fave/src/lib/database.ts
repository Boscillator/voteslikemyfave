import neo4j from 'neo4j-driver';

const neo4j_uri = process.env.NEO4J_URI!;
const neo4j_username = process.env.NEO4J_USER || 'neo4j';
const neo4j_password = process.env.NEO4J_PASSWORD!;
const driver = neo4j.driver(neo4j_uri, neo4j.auth.basic(neo4j_username, neo4j_password));

export type LegislatorSummary = {
  bioguide_id: string,
  given_name: string,
  family_name: string,
  state: string,
  party: string
};

export const CURRENT_CONGRESS = parseInt(process.env.CURRENT_CONGRESS || '119');

export async function list_legislators_by_congress(congress:number): Promise<LegislatorSummary[]> {
  const query = `
    MATCH (l: Legislator)-[:VOTED_ON]-(:RollCall { congress: $congress})
    MATCH (l)-[:CURRENTLY_MEMBER_OF]->(p: Party)
    MATCH (l)-[:CURRENTLY_REPRESENTS]->(s: State)
    RETURN DISTINCT l.bioguide_id as bioguide_id, l.given_name as given_name, l.family_name as family_name, s.code as state, p.abbreviation as party
  `;

  const { records } = await driver.executeQuery(query, {congress});
  return records.map(r => r.toObject() as LegislatorSummary);
}
