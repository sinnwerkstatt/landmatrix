import { stringify as csvStringify } from "csv-stringify/browser/esm/sync"
import * as xlsx from "xlsx"

import type { Country, Region } from "$lib/types/data"

import { type FileType } from "$components/New/DownloadModal.svelte"

import type { CaseStatisticsObject } from "./CaseStatisticsTable.svelte"
import type { Filters } from "./FilterBar.svelte"

export const createBlob: <T>(fileType: FileType, objects: T[]) => Blob | void = (
  fileType,
  objects,
) => {
  //eslint-disable-next-line @typescript-eslint/no-explicit-any
  const blobFns: { [key in FileType]: (objects: any[]) => void } = {
    csv: objects => {
      const csvString = csvStringify(objects, { header: true })
      return new Blob([csvString], { type: "text/csv" })
    },
    xlsx: objects => {
      const csvString = csvStringify(objects, { header: true })
      const wb = xlsx.read(csvString, { type: "string" })
      const data = xlsx.write(wb, { type: "array", bookType: "xlsx" })
      return new Blob([data], { type: "application/ms-excel" })
    },
    json: () => {
      throw new Error("NOT IMPLEMENTED")
    },
  }
  return blobFns[fileType](objects)
}

export const createLookup = <T extends Record<"id", string | number>>(
  objects: T[],
): { [id: string | number]: T } =>
  objects.reduce((acc, val) => ({ ...acc, [val.id]: val }), {})

export const resolveCountryAndRegionNames = (
  objects: CaseStatisticsObject[],
  relatedObjects: {
    countries: Country[]
    regions: Region[]
  },
): (Omit<CaseStatisticsObject, "country_id" | "region_id"> & {
  country?: string
  region?: string
})[] => {
  const countryLookup = createLookup(relatedObjects.countries)
  const regionLookup = createLookup(relatedObjects.regions)

  return objects.map(o => {
    const { country_id, region_id, ...rest } = o
    return {
      ...rest,
      country: countryLookup[country_id!]?.name,
      region: regionLookup[region_id!]?.name,
    }
  })
}

export const createCountyRegionSuffix = (filters: Filters) =>
  filters.country
    ? filters.country.name
    : filters.region
      ? filters.region.name
      : "Global"

export const createDateString = () => new Date().toISOString().slice(0, 10)

export const createFilename = (
  basename: string,
  filters: Filters,
  fileType: FileType,
) =>
  [createDateString(), basename, createCountyRegionSuffix(filters)]
    .join("_")
    .replaceAll(" ", "-") +
  "." +
  fileType
