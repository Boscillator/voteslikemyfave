import { CURRENT_CONGRESS, LegislatorSummary, list_legislators_by_congress } from "@/lib/database";
import { GetStaticProps, InferGetStaticPropsType } from "next";
import { MagnifyingGlassIcon } from "@heroicons/react/24/solid";
import React from "react";

const NUM_SEARCH_RESULTS = 3;

export default function Home({ legislators }: InferGetStaticPropsType<typeof getStaticProps>) {
  const [searchResults, setSearchResult] = React.useState(legislators.slice(0,NUM_SEARCH_RESULTS));

  const onSearchChange = (content: string) => {
    const normalizedContent = content.toLowerCase();
    const candidateResults = legislators.filter(l => {
      return (l.family_name.toLowerCase().indexOf(normalizedContent) != -1) || (l.given_name.toLowerCase().indexOf(normalizedContent) != -1);
    })

    setSearchResult(candidateResults.slice(0,NUM_SEARCH_RESULTS));
  };

  return (
    <div>
      <div className="flex justify-center h-screen bg-gray-100">
        <SearchBox results={searchResults} onSearchChange={onSearchChange} />
      </div>
    </div>
  );
}

export const getStaticProps = (async () => {
  const legislators = await list_legislators_by_congress(CURRENT_CONGRESS);
  return { props: { legislators } };
}) satisfies GetStaticProps<{ legislators: LegislatorSummary[] }>

interface SearchBoxProps {
  results: LegislatorSummary[],
  onSearchChange: (text: string) => void
}

function SearchBox({ results, onSearchChange }: SearchBoxProps) {
  "use client";
  const container: React.Ref<HTMLDivElement|null> = React.useRef(null);
  const [focused, setFocus] = React.useState(false);

  const onFocus = () => setFocus(container.current!.contains(document.activeElement));
  const onBlur = () => setFocus(container.current!.contains(document.activeElement));

  return (
    <div className="relative w-full max-w-xl pt-40">
      <div className="relative shadow-md" ref={container} onFocus={onFocus} onBlur={onBlur}>
        <input
          type="text"
          placeholder="Search..."
          className={"w-full p-3 pl-5 text-lg border focus:outline-none " + (focused ? "rounded-t-md" : "rounded-md")}
          onChange={(e) => onSearchChange(e.target.value)}
          />

        <button className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-blue-500 p-2 rounded-full text-white hover:ring-2 hover:scale-110 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent">
          <MagnifyingGlassIcon className="w-6 h-6" />
        </button>

        {focused ?
          <div className="absolute w-full border  bg-white rounded-b-md">
            <ul className="divide-y divide-gray-200">
              {results.map(r =>
                <SearchResult result={r} />
              )}
            </ul>
          </div> : null
        }
      </div>
    </div>
  );
}

interface SearchResultProps {
  result: LegislatorSummary
}

function SearchResult({ result }: SearchResultProps) {
  return <li key={result.bioguide_id} className="hover:bg-gray-100 cursor-pointer">
    <button className="w-full h-full p-3 pl-5 text-left">{result.family_name}, {result.given_name} ({result.party}-{result.state})</button>
  </li>;
}

