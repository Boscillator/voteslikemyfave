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
