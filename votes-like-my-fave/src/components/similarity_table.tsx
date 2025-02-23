import { SimilarityStatistics } from "@/lib/database";
import { LegislatorIcon, StyledLink } from "./legislator_utilities";

export const LegislatorSimilarityTable: React.FC<{ data: SimilarityStatistics }> = ({ data }) => {
  return (
    <div className="overflow-x-auto p-4">
      <table className="min-w-full border border-gray-200 shadow-md rounded-lg">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 border">Image</th>
            <th className="px-4 py-2 border">Legislator</th>
            <th className="px-4 py-2 border">Voted The Same As</th>
            <th className="px-4 py-2 border">Votes Differently Than</th>
            <th className="px-4 py-2 border">% Agreement</th>
          </tr>
        </thead>
        <tbody>
          {data.similarity.map((item) => (
            <tr key={item.other.bioguide_id} className="odd:bg-white even:bg-gray-50">
              <td className="px-4 py-2 border text-center">
                <LegislatorIcon legislator={item.other} center={true}/>
              </td>
              <td className="px-4 py-2 border">
                <StyledLink href={"/" + item.other.state + "/" + item.other.family_name}> {item.other.family_name}, {item.other.given_name} ({item.other.state}-{item.other.party})</StyledLink>
              </td>
              <td className="px-4 py-2 border text-center">{item.votes_together} times</td>
              <td className="px-4 py-2 border text-center">{item.votes_against} times</td>
              <td className="px-4 py-2 border text-center">{(100 * item.percent_agreement).toFixed(0)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
