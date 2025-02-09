// Votes against party
MATCH (p: Party {abbreviation: "D"})
MATCH (l: Legislator)-[:CURRENTLY_MEMBER_OF]->(p)
MATCH (l)-[vote:VOTED_ON]->(rc: RollCall)
WITH rc, vote.vote as vote, count(vote.vote) as vote_count
WITH rc, apoc.agg.maxItems(vote, vote_count) as max_data
MATCH (l: Legislator)-[:CURRENTLY_MEMBER_OF]-(p: Party {abbreviation: "D"})
MATCH (l)-[vote:VOTED_ON]->(rc)
WITH l, sum(toInteger(vote.vote <> max_data.items[0])) as votes_against, count(vote) as total_votes
RETURN l.given_name, l.family_name, votes_against, toFloat(votes_against)/total_votes as percent_against
ORDER BY percent_against DESC

// Member for lastname/state/party
MATCH (l: Legislator { family_name: "Raskin"})
      , (l)-[:CURRENTLY_MEMBER_OF]->(:Party {abbreviation: "D"})
      , (l)-[:CURRENTLY_REPRESENTS]-(:State {code: "MD"})
RETURN l

// jacard index
MATCH (l1: Legislator { bioguide_id: "R000606" })
MATCH (l1)-[v1:VOTED_ON]-(rc: RollCall)
      , (l2)-[v2: VOTED_ON]-(rc)
WITH l2, sum(toInteger(v1.vote = v2.vote)) as votes_together, sum(toInteger(v1.vote <> v2.vote)) as votes_againsts
WITH *, votes_together + votes_againsts as votes_total
WITH *, toFloat(votes_together) / votes_total as percent_agreement
MATCH (l2)-[:CURRENTLY_MEMBER_OF]-(p: Party)
MATCH (l2)-[:CURRENTLY_REPRESENTS]-(s: State)
RETURN l2.bioguide_id as bioguide_id
       , l2.family_name as family_name
       , p.abbreviation as party
       , s.code as state
       , votes_together
       , votes_againsts
       , votes_total
       , percent_agreement
ORDER BY percent_agreement
