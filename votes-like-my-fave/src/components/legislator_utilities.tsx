import { BIOGUIDE_PHOTO_ROOT, LegislatorSummary } from "@/lib/database";

export type LegislatorIconProps = {
  legislator: LegislatorSummary
};

export function LegislatorIcon({ legislator: legislator }: LegislatorIconProps) {
  return <img
    src={BIOGUIDE_PHOTO_ROOT + legislator.image}
    alt={`${legislator.given_name} ${legislator.family_name}`}
    className="w-12 h-12 rounded-full mx-auto"
  />
}
