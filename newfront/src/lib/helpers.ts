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

export function isEmpty(field: unknown): boolean {
  return (
    field === undefined ||
    field === null ||
    field === "" ||
    (Array.isArray(field) && field.length === 0)
  );
}
