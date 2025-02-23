import { BIOGUIDE_PHOTO_ROOT, CURRENT_CONGRESS, get_legislator_by_congress_name_and_state, LegislatorDetails, list_legislators_by_congress } from "@/lib/database";
import { GetStaticProps, InferGetStaticPropsType } from "next";
import { notFound } from "next/navigation";

export default function Legislator({ details } : InferGetStaticPropsType<typeof getStaticProps>) {
  if(details === undefined) {
    notFound();
  }

  const legislator = details.legislator;


  return (<div className="m-auto max-w-6xl mt-16 shadow-md border-r-8 flex flex-col rounded-lg border-none">
    <div className="bg-blue-900 rounded-t-lg p-2">
      <h1 className="text-2xl text-white font-bold">{legislator.family_name}, {legislator.given_name} ({details.party.abbreviation}-{details.state.code})</h1>
    </div>
    <div>
      <img className="h-full m-4" src={BIOGUIDE_PHOTO_ROOT + legislator.image} />
    </div>
  </div>)
}


export const getStaticProps = (async (context) => {
  const last_name = context.params?.lastname as string;
  const state = context.params?.state as string;
  const details = await get_legislator_by_congress_name_and_state(CURRENT_CONGRESS, last_name, state);

  if (details === undefined) {
    return {props: {details: undefined}};
  }
  
  return { props: { details } };
}) satisfies GetStaticProps<{ details: LegislatorDetails | undefined }>

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
