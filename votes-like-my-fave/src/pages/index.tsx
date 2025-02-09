import { CURRENT_CONGRESS, LegislatorSummary, list_legislators_by_congress } from "@/lib/database";
import { GetStaticProps, InferGetServerSidePropsType } from "next";

export default function Home({legislators}: InferGetServerSidePropsType<typeof getStaticProp>) {
  return (
    <div>
      <h1>Hello World</h1>
      <ul>
        {legislators.map(l => <li key={l.bioguide_id}>{l.family_name} ({l.party}-{l.state})</li>)}
      </ul>
    </div>
  );
}

export const getStaticProps = (async () => {
  const legislators = await list_legislators_by_congress(CURRENT_CONGRESS);
  return {props: {legislators}};
}) satisfies GetStaticProps<{legislators: LegislatorSummary[]}>
