interface Legislator {
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

interface IsRelatedTo {
  relationship_type: string;
}

interface Congress {
  number: number;
  start_date?: string; // Date type in TypeScript can be string or Date
  end_date?: string;
}

interface IsMemberOfCongress {
  parties: string[];
}

interface Party {
  name: string;
  abbreviation?: string;
}

interface IsMemberOfParty {}

interface State {
  code: string;
}

interface Represents {}

enum Chamber {
  HOUSE_OF_REPS = "house",
  SENATE = "senate"
}

interface RollCall {
  chamber: Chamber;
  congress: number;
  session: number;
  number: number;
  when: string; // Use string for ISO date representation
  question: string;
}

interface VotedOn {
  vote: string;
}