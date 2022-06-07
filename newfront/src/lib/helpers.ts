// import { get } from "svelte/store";
// import { countries, regions } from "$lib/stores";
// import type { CountryOrRegion } from "./types/wagtail";
// export function getCountryOrRegion(
//   id: number,
//   region = false
// ): CountryOrRegion | undefined {
//   return region
//     ? get(regions).find((region) => region.id === +id)
//     : get(countries).find((country) => country.id === +id);
// }
import { nanoid } from "nanoid";

export function isEmpty(field: unknown): boolean {
  return (
    field === undefined ||
    field === null ||
    field === "" ||
    (Array.isArray(field) && field.length === 0)
  );
}

export function newNanoid(existingIDs: string[]): string {
  let newID: string;
  let matching: boolean;
  do {
    newID = nanoid(8);
    matching = existingIDs.includes(newID);
  } while (matching);
  return newID;
}
