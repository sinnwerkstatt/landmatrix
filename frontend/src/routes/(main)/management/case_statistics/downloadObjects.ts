import { stringify as csvStringify } from "csv-stringify/browser/esm/sync"
import * as xlsx from "xlsx"

import type { FilterValues } from "$lib/filters"
import type { Country, Region } from "$lib/types/data"

import { type FileType } from "$components/New/DownloadModal.svelte"

import type { CaseStatisticsObject } from "./CaseStatisticsTable.svelte"

export const createBlob = (fileType: FileType, data: unknown): Blob => {
  switch (fileType) {
    case "json": {
      const jsonString = JSON.stringify(data)
      return new Blob([jsonString], { type: "application/json" })
    }
    case "csv": {
      const csvString = csvStringify([data], { header: true })
      return new Blob([csvString], { type: "text/csv" })
    }
    case "xlsx": {
      const csvString = csvStringify([data], { header: true })
      const wb = xlsx.read(csvString, { type: "string" })
      const wbString = xlsx.write(wb, { type: "array", bookType: "xlsx" })
      return new Blob([wbString], { type: "application/ms-excel" })
    }
  }
}

type Lookup<T> = { [id: string | number]: T }

export type DownloadContext = {
  filters: FilterValues
  countries: Country[]
  regions: Region[]
}

export const createLookup = <T extends Record<"id", string | number>>(
  objects: T[],
): Lookup<T> => objects.reduce((acc, val) => ({ ...acc, [val.id]: val }), {})

export const resolveCountryAndRegionNames = (
  objects: CaseStatisticsObject[],
  context: DownloadContext,
): (Omit<CaseStatisticsObject, "country_id" | "region_id"> & {
  country?: string
  region?: string
})[] => {
  const countryLookup = createLookup(context.countries)
  const regionLookup = createLookup(context.regions)

  return objects.map(o => {
    const { country_id, region_id, ...rest } = o
    return {
      ...rest,
      country: countryLookup[country_id!]?.name,
      region: regionLookup[region_id!]?.name,
    }
  })
}

export const createCountyRegionSuffix = (context: DownloadContext) => {
  const countryLookup = createLookup(context.countries)
  const regionLookup = createLookup(context.regions)

  const filters = context.filters

  return filters.country_id
    ? countryLookup[filters.country_id!]?.name
    : filters.region_id
      ? regionLookup[filters.region_id!]?.name
      : "Global"
}
export const createDateString = () => new Date().toISOString().slice(0, 10)

export const createFilename = (
  basename: string,
  fileType: FileType,
  context: DownloadContext,
) =>
  [createDateString(), basename, createCountyRegionSuffix(context)]
    .join("_")
    .replaceAll(" ", "-") +
  "." +
  fileType
