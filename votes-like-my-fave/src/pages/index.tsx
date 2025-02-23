import { BIOGUIDE_PHOTO_ROOT, CURRENT_CONGRESS, LegislatorSummary, list_legislators_by_congress } from "@/lib/database";
import { GetStaticProps, InferGetStaticPropsType } from "next";
import { MagnifyingGlassIcon } from "@heroicons/react/24/solid";
import React, { FormEvent, Fragment } from "react";
import { useRouter } from "next/navigation";

const NUM_SEARCH_RESULTS = 3;

export default function Home({ legislators }: InferGetStaticPropsType<typeof getStaticProps>) {
  return (
    <Fragment>
      <div className="flex justify-center">
        <SearchBox legislators={legislators} />
      </div>
    </Fragment>
  );
}

export const getStaticProps = (async () => {
  const legislators = await list_legislators_by_congress(CURRENT_CONGRESS);
  return { props: { legislators } };
}) satisfies GetStaticProps<{ legislators: LegislatorSummary[] }>

interface SearchBoxProps {
  legislators: LegislatorSummary[]
}

function SearchBox({ legislators }: SearchBoxProps) {
  const [searchResults, setSearchResult] = React.useState(legislators.slice(0, NUM_SEARCH_RESULTS));
  const router = useRouter();

  const onSearchChange = (content: string) => {
    const normalizedContent = content.toLowerCase();
    const candidateResults = legislators.filter(l => {
      return (l.family_name.toLowerCase().indexOf(normalizedContent) != -1) || (l.given_name.toLowerCase().indexOf(normalizedContent) != -1);
    })

    setSearchResult(candidateResults.slice(0, NUM_SEARCH_RESULTS));
  };

  const onSubmit = (legislator: LegislatorSummary | undefined) => {
    if (legislator === undefined) {
      return;
    }

    const path = `/${legislator.state}/${legislator.family_name}`
    router.push(path);
  }

  return (
    <div className="flex w-full justify-center h-screen bg-gray-100">
      <SearchBoxStyle results={searchResults} onSearchChange={onSearchChange} onSubmit={onSubmit} />
    </div>
  );
}

interface SearchBoxStyleProps {
  results: LegislatorSummary[],
  onSearchChange: (text: string) => void,
  onSubmit: (legislator: LegislatorSummary | undefined) => void
}

function SearchBoxStyle({ results, onSearchChange, onSubmit }: SearchBoxStyleProps) {
  const container: React.Ref<HTMLFormElement | null> = React.useRef(null);

  const onSubmitHandler = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(results.at(0));
  };

  const onResultSelect = (l: LegislatorSummary) => {
    onSubmit(l);
  }

  return (
    <div className="relative w-full max-w-xl pt-10">
      <form className="relative shadow-md group search-box" ref={container} onSubmit={onSubmitHandler}>
        <input
          type="text"
          placeholder="Search..."
          className={"w-full p-3 pl-5 text-lg border focus:outline-none"}
          onChange={(e) => onSearchChange(e.target.value)}
        />

        <button type="submit" name="default_submit" value={results.at(0)?.bioguide_id} className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-blue-500 p-2 rounded-full text-white hover:ring-2 hover:scale-110 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent">
          <MagnifyingGlassIcon className="w-6 h-6" />
        </button>

        <div className="absolute group-focus-within:block hidden w-full border  bg-white rounded-b-md">
          <ul className="divide-y divide-gray-200">
            {results.map(r =>
              <SearchResult key={r.bioguide_id} result={r} onResultSelect={onResultSelect} />
            )}
          </ul>
        </div>
      </form>
    </div>
  );
}

interface SearchResultProps {
  result: LegislatorSummary,
  onResultSelect: (legislator: LegislatorSummary) => void
}

function SearchResult({ result, onResultSelect }: SearchResultProps) {
  const onClick = () => {
    onResultSelect(result);
  };

  const image_url = BIOGUIDE_PHOTO_ROOT + result.image;

  return <li className="hover:bg-gray-100 cursor-pointer">
    <button type="button" className="flex w-full h-full p-3 pl-5 text-left items-center gap-5" onClick={onClick}>
      <img className="h-10 w-10 rounded-full" src={image_url} />
      <div className="text-xl">{result.family_name}, {result.given_name} ({result.party}-{result.state})</div>
    </button>
  </li>;
}

