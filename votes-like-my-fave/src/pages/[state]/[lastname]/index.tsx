import { LegislatorSimilarityTable } from "@/components/similarity_table";
import { BIOGUIDE_PHOTO_ROOT, CURRENT_CONGRESS, get_legislator_by_congress_name_and_state, getSimilaritiesFor, LegislatorDetails, list_legislators_by_congress, SimilarityStatistics, VotePartySummaryForRepublicansAndDemocrats, votePartySummaryForRepublicansAndDemocrats } from "@/lib/database";
import { ColorClassPrefix, partyToColorClass } from "@/lib/utilities";
import { GetStaticProps, InferGetStaticPropsType } from "next";
import { notFound } from "next/navigation";
import React from "react";

type LinearMeterProps = {
  label: string;
  value: number;
  max: number;
  color: 'red' | 'blue'
};

const LinearMeter: React.FC<LinearMeterProps> = ({ label, value, max, color }) => {
  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 ">
        {label}
      </label>
      <div className="relative w-full h-6 bg-gray-200 rounded-lg overflow-hidden text-white">
        <div
          className={"h-full transition-all pl-4 bg-" + color + "-900"}
          style={{ width: `${(value / max) * 100}%` }}
        >
          {value} / {max}
        </div>
      </div>
    </div>
  );
};

export default function Legislator({ details, vote_summary, similarities }: InferGetStaticPropsType<typeof getStaticProps>) {
  if (details === undefined || vote_summary === undefined) {
    notFound();
  }

  const legislator = details.legislator;


  return (<div className="m-auto max-w-6xl mt-10 shadow-md border-r-8 flex flex-col rounded-lg border-none">
    <div className={"rounded-t-lg p-2 " + partyToColorClass(ColorClassPrefix.bg, details.party)}>
      <h1 className="text-2xl text-white font-bold">{legislator.family_name}, {legislator.given_name} ({details.party.abbreviation}-{details.state.code})</h1>
    </div>
    <div className="flex flex-row gap-4">
      <img className="m-4 min-w-[200px]" width="200" src={BIOGUIDE_PHOTO_ROOT + legislator.image} />
      <div className="p-4 space-y-4 flex-grow">
        <LinearMeter label="Votes With Majority of Republicans" value={vote_summary.republican.votes_with} max={vote_summary.republican.total_votes} color="red" />
        <LinearMeter label="Votes With Majority of Democrats" value={vote_summary.democrat.votes_with} max={vote_summary.democrat.total_votes} color="blue" />
        <p className="text-xs"><b>Profile:</b> {legislator.profile_text}</p>
      </div>
    </div>
    <div>
      <LegislatorSimilarityTable data={similarities}/>
    </div>
  </div>);
}


export const getStaticProps = (async (context) => {
  const last_name = context.params?.lastname as string;
  const state = context.params?.state as string;
  const details = await get_legislator_by_congress_name_and_state(CURRENT_CONGRESS, last_name, state);

  if (details === undefined) {
    return { props: { details: undefined, vote_summary: undefined } };
  }

  const vote_summary = await votePartySummaryForRepublicansAndDemocrats(details.legislator.bioguide_id);
  if (vote_summary === undefined) {
    return { props: { details: details, vote_summary: undefined } };
  }

  const similarities = await getSimilaritiesFor(details.legislator.bioguide_id);

  return { props: { details, vote_summary, similarities } };
}) satisfies GetStaticProps<{ 
  details: LegislatorDetails | undefined,
  vote_summary: VotePartySummaryForRepublicansAndDemocrats | undefined,
  similarities: SimilarityStatistics }>

export const getStaticPaths = (async () => {
  const legislators = await list_legislators_by_congress(CURRENT_CONGRESS);
  return {
    paths: legislators.map(l => ({
      params: {
        lastname: l.family_name,
        state: l.state
      }
    })),
    fallback: false
  }
});
