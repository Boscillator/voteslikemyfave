export interface Legislator {
  bioguide_id: string;
  family_name: string;
  given_name: string;
  unaccented_family_name: string;
  unaccented_given_name: string;
  profile_text: string;
  image?: string;
  middle_name?: string;
  unaccented_middle_name?: string;
  nick_name?: string;
  honorific_prefix?: string;
  honorific_suffix?: string;
  birth_date?: string;
  birth_circa?: boolean;
  birth_date_unknown?: boolean;
  death_date?: string;
  death_circa?: boolean;
  death_date_unknown?: boolean;
}

export interface IsRelatedTo {
  relationship_type: string;
}

export interface Congress {
  number: number;
  start_date?: string; // Date type in TypeScript can be string or Date
  end_date?: string;
}

export interface IsMemberOfCongress {
  parties: string[];
}

export interface Party {
  name: string;
  abbreviation?: string;
}

export interface IsMemberOfParty {
  // Place holder for when attributes are added
}

export interface State {
  code: string;
}

export interface Represents {
  // Place holder for when attributes are added
}

export enum Chamber {
  HOUSE_OF_REPS = "house",
  SENATE = "senate"
}

export interface RollCall {
  chamber: Chamber;
  congress: number;
  session: number;
  number: number;
  when: string; // Use string for ISO date representation
  question: string;
}

export interface VotedOn {
  vote: string;
}