// const myMixin = {
//   data() {
//     return {
//       current: -1,
//       vals:
//         this.value && this.value.length > 0
//           ? JSON.parse(JSON.stringify(this.value))
//           : [{}],
//     };
//   },
//   created() {
//     if (this.value) {
//       this.current = this.value.map((e) => e.current).indexOf(true);
//     }
//   },
import { _ } from "svelte-i18n";
import { get } from "svelte/store";
import type {
  ImplementationStatus,
  IntentionOfInvestment,
  NegotiationStatus,
} from "../../../lib/filters";

export function dateCurrentFormat(value: { date: string; current?: boolean }): string {
  if (!value.date && !value.current) return "";
  let ret = "[";
  if (value.date) ret += value.date;
  if (value.date && value.current) ret += ", ";
  if (value.current) ret += get(_)("current");
  ret += "]";
  return ret;
}

export function mapChoices(choices, formfieldChoices) {
  let ret = "";
  if (choices instanceof Array) {
    ret += choices.map((v) => formfieldChoices[v]).join(", ");
  } else {
    ret += formfieldChoices[choices];
  }
  return ret;
}

export function parseValues(jsonval) {
  let ret = "";
  const choices = this.formfield.choices;

  if (jsonval.value instanceof Array) {
    if (choices) {
      ret += jsonval.value.map((v) => choices[v]).join(", ");
    } else ret += jsonval.value.join(", ");
  } else {
    if (choices) ret += choices[jsonval.value];
    else ret += jsonval.value;
  }
  return ret;
}

export function updateCurrent(i) {
  this.current = i;
  this.updateEntries();
}

export function updateEntries() {
  this.vals = this.vals.map((v, i) => {
    const current = i === this.current ? { current: true } : {};
    delete v.current;
    return { ...v, ...current };
  });
  this.$emit("input", this.filteredVals);
}
export function addEntry() {
  this.current = null;
  this.vals.push({});
  this.updateEntries();
}

export function removeEntry(index) {
  if (this.current === this.vals.length - 1) this.current = null;
  this.vals.splice(index, 1);
  this.updateEntries();
}

enum ActorRole {
  TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES = "TRADITIONAL_LAND_OWNERS_OR_COMMUNITIES",
  GOVERNMENT_OR_STATE_INSTITUTIONS = "GOVERNMENT_OR_STATE_INSTITUTIONS",
  TRADITIONAL_LOCAL_AUTHORITY = "TRADITIONAL_LOCAL_AUTHORITY",
  BROKER = "BROKER",
  INTERMEDIARY = "INTERMEDIARY",
  OTHER = "OTHER",
}

export type JSONActorsFieldType = {
  name: string;
  role: ActorRole;
};

export type JSONDateAreaChoicesFieldType = {
  current?: boolean;
  name: string;
  area?: string;
  choices: Array<IntentionOfInvestment | { [key: string]: string }>;
};

export type JSONDateAreaFieldType = {
  area: string;
  date: string;
  current?: boolean;
};

export type JSONDateChoiceFieldType = {
  current?: boolean;
  date: string;
  choice: NegotiationStatus | ImplementationStatus;
};
export type JSONExportsFieldType = {
  current?: boolean;
  area?: string;
  yield?: string;
  export?: string;
  choices: Array<{ [key: string]: string }>;
};

// folgende types möglicherweise fehlerhaft oder unvollständig
export type JSONFieldType = {
  current?: boolean;
  area?: string;
  choices?: Array<{ [key: string]: string }>;
};

export type JSONJobsFieldType = {
  current?: boolean;
  date: string;
  jobs?: string;
  employees?: string;
  workers?: string;
  choices?: Array<{ [key: string]: string }>;
};

export type JSONLeaseFieldType = {
  current?: boolean;
  date: string;
  area?: string;
  farmers: string;
  households: string;
};
