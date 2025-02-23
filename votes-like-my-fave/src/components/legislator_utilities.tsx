import { BIOGUIDE_PHOTO_ROOT, LegislatorSummary } from "@/lib/database";
import { ArrowTopRightOnSquareIcon } from "@heroicons/react/24/solid";

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

export function ExternalLink({ text, href, gray}: { text: string; href: string; gray?: number; }) {
  gray = gray || 700;
  return (
    <a className={"inline underline hover:text-gray-" + gray} href={href}><ArrowTopRightOnSquareIcon className="inline h-4 px-1 self-center"/>{text}</a>
  );
}

export function SourceDisclaimer() {

  return <p className="text-xs">
    <b>Data from: </b>
    <ExternalLink text="bioguide.congress.gov" href="https://bioguide.congress.gov" />, <ExternalLink href="https://www.senate.gov/legislative/votes_new.htm" text="senate.gov" /> and <ExternalLink href="https://www.congress.gov/roll-call-votes" text="congress.gov" />
  </p>
}
