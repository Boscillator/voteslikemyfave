import neo4j, { NotificationFilterMinimumSeverityLevel } from 'neo4j-driver';
import { Legislator, Party, State } from './models';

export const CURRENT_CONGRESS = parseInt(process.env.CURRENT_CONGRESS || '119');
export const BIOGUIDE_PHOTO_ROOT = process.env.BIOGUIDE_PHOTO_ROOT || 'https://bioguide.congress.gov/photo/';
const neo4j_uri = process.env.NEO4J_URI || 'neo4j://database:7687';
const neo4j_username = process.env.NEO4J_USER || 'neo4j';
const neo4j_password = process.env.NEO4J_PASSWORD!;

const driver = neo4j.driver(neo4j_uri, neo4j.auth.basic(neo4j_username, neo4j_password), { disableLosslessIntegers: true });

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

export type LegislatorDetails = {
  legislator: Legislator,
  party: Party,
  state: State
};

export async function get_legislator_by_congress_name_and_state(congress: number, family_name: string, state: string): Promise<LegislatorDetails | undefined> {
  const query = `
    MATCH (l: Legislator { family_name: $family_name})
      , (l)-[:CURRENTLY_REPRESENTS]->(s: State { code: $state })
      , (l)-[:IS_MEMBER_OF_CONGRESS]->(:Congress { number: $congress })
      , (l)-[:CURRENTLY_MEMBER_OF]->(p: Party)
    LIMIT 1
    RETURN l as legislator, p as party, s as state
  `;
  const { records } = await driver.executeQuery(query, {congress, family_name, state});
  const results = records.map(r => {
    const obj = r.toObject();
    return {
      legislator: obj.legislator.properties as Legislator,
      party: obj.party.properties as Party,
      state: obj.state.properties as State
    }
  });

  return results.at(0);
}

export type VotePartySummary = {
  votes_with: number,
  votes_against: number,
  total_votes: number,
  percent_with: number
};

export async function voteSummaryByParty(bioguide_id: string, party_abbr: string): Promise<VotePartySummary | undefined> {
  const query = `
    MATCH (p: Party {abbreviation: $party_abbr})
    MATCH (l: Legislator)-[:CURRENTLY_MEMBER_OF]->(p)
    MATCH (l)-[vote:VOTED_ON]->(rc: RollCall)
    WITH rc, vote.vote as vote, count(vote.vote) as vote_count
    WITH rc, apoc.agg.maxItems(vote, vote_count) as max_data
    MATCH (l: Legislator { bioguide_id: $bioguide_id })
    MATCH (l)-[vote:VOTED_ON]->(rc)
    WHERE vote.vote <> "Not Voting"
    WITH l, sum(toInteger(vote.vote = max_data.items[0])) as votes_with, count(vote) as total_votes
    RETURN votes_with
        , total_votes
        , toFloat(votes_with)/total_votes as percent_with
        , total_votes - votes_with as votes_against
    LIMIT 1
  `;

  const { records } = await driver.executeQuery(query, {bioguide_id, party_abbr});
  const results = records.map(r => r.toObject() as VotePartySummary);
  return results.at(0);
}

export type VotePartySummaryForRepublicansAndDemocrats = {
  republican: VotePartySummary,
  democrat: VotePartySummary
};

export async function votePartySummaryForRepublicansAndDemocrats(bioguide_id: string): Promise<VotePartySummaryForRepublicansAndDemocrats | undefined> {
  const republicans_promise = voteSummaryByParty(bioguide_id, "R");
  const democrat_promise = voteSummaryByParty(bioguide_id, "D");
  const [republican, democrat] = await Promise.all([republicans_promise, democrat_promise]);

  if(republican === undefined || democrat === undefined) {
    return undefined;
  }

  return {republican, democrat};
}
