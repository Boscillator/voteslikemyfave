import { BIOGUIDE_PHOTO_ROOT, LegislatorSummary } from "@/lib/database";

export type LegislatorIconProps = {
  legislator: LegislatorSummary,
  center?: boolean
};

export function LegislatorIcon({ legislator, center}: LegislatorIconProps) {
  const centerClass = center ? "mx-auto" : "";
  return <img
    src={BIOGUIDE_PHOTO_ROOT + legislator.image}
    alt={`${legislator.given_name} ${legislator.family_name}`}
    className={"w-12 h-12 rounded-full object-fit-none " + centerClass}
  />
}

export function SourceDisclaimer() {
  const SourceLink = ({text, href}: {text: string, href: string}) => (
    <a className="inline underline hover:text-gray-700" href={href}>{text}</a>
  );

  return <p className="text-xs">
    <b>Data from: </b>
    <SourceLink text="bioguide.congress.gov" href="https://bioguide.congress.gov" />, <SourceLink href="https://www.senate.gov/legislative/votes_new.htm" text="senate.gov" /> and <SourceLink href="https://www.congress.gov/roll-call-votes" text="congress.gov" />
  </p>
}
