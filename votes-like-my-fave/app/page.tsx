import Image from "next/image";
import { CURRENT_CONGRESS, LegislatorSummary, list_legislators_by_congress } from "@/lib/database";

type Props = {
  legislators: LegislatorSummary[]
}

export default async function Home() {
  const legislators = await list_legislators_by_congress(CURRENT_CONGRESS);
  return (
    <div>
      <h1>Hello World</h1>
      <ul>{ legislators.map(l => <li key={l.bioguide_id}>{l.family_name}</li>) }</ul>
    </div>
  );
}
