import {Party} from "@/lib/models"

export enum ColorClassPrefix {
  text = "text",
  bg = "bg"
};

export function partyToColorClass(prefix: ColorClassPrefix, party: Party) {
  if(party.abbreviation === "R") {
    return prefix + "-red-900";
  } else if(party.abbreviation === "D") {
    return prefix + "-blue-900";
  } else {
    return prefix + "-green-900";
  }
}
