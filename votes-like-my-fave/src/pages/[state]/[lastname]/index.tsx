import { useRouter } from "next/router";
import { CURRENT_CONGRESS, get_legislator_by_congress_name_and_state, list_legislators_by_congress } from "@/lib/database";
import { GetStaticProps, InferGetStaticPropsType } from "next";
import { notFound } from "next/navigation";

export default function Legislator({legislator } : InferGetStaticPropsType<typeof getStaticProps>) {
  if(legislator === undefined) {
    notFound();
  }

  return <p>{legislator?.family_name}</p>
}


export const getStaticProps = (async (context) => {
  const last_name = context.params?.lastname as string;
  const state = context.params?.state as string;
  const legislator = await get_legislator_by_congress_name_and_state(CURRENT_CONGRESS, last_name, state);

  if (legislator === undefined) {
    return {props: {legislator: undefined}};
  }
  
  return { props: { legislator } };
}) satisfies GetStaticProps<{ legislator: Legislator | undefined }>

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
