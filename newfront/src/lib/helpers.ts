import { get } from "svelte/store";
import { countries, regions } from "$lib/stores";
import type { CountryOrRegion } from "$lib/types/custom";

export function getCountryOrRegion(
  id: number,
  region = false
): CountryOrRegion | undefined {
  return region
    ? get(regions).find((region) => region.id === +id)
    : get(countries).find((country) => country.id === +id);
}
