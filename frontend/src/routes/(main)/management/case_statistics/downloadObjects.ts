import { stringify as csvStringify } from "csv-stringify/browser/esm/sync"
import { get } from "svelte/store"
import * as xlsx from "xlsx"

import { page } from "$app/stores"

import type { Country, Model, Region } from "$lib/types/data"

import { type FileType } from "$components/New/DownloadModal.svelte"

import { aDownload } from "../downloadObjects"
import type { CaseStatisticsObject } from "./CaseStatisticsTable.svelte"
import type { Filters } from "./FilterBar.svelte"

export const downloadFns: {
  [key in FileType]: (objects: CaseStatisticsObject[], filename: string) => void
} = {
  csv: (objects, filename) => {
    const csvString = csvStringify(objects, { header: true })
    const blob = new Blob([csvString], { type: "text/csv" })

    aDownload(blob, `${filename}.csv`)
  },
  xlsx: (objects, filename) => {
    const csvString = csvStringify(objects, { header: true })
    const wb = xlsx.read(csvString, { type: "string" })
    const data = xlsx.write(wb, { type: "array", bookType: "xlsx" })
    const blob = new Blob([data], { type: "application/ms-excel" })

    aDownload(blob, `${filename}.xlsx`)
  },
  json: () => {
    throw new Error("NOT IMPLEMENTED")
  },
}

export const downloadEnriched = (
  fileType: FileType,
  filename: string,
  objects: CaseStatisticsObject[],
) => {
  const countryLookup: { [key: number]: Country } = get(page).data.countries.reduce(
    (acc, val) => ({ ...acc, [val.id]: val }),
    {},
  )
  const regionLookup: { [key: number]: Region } = get(page).data.regions.reduce(
    (acc, val) => ({ ...acc, [val.id]: val }),
    {},
  )

  const enriched = objects.map(o => ({
    ...o,
    // country_id: undefined,
    // region_id: undefined,
    country: countryLookup[o.country_id!]?.name,
    region: regionLookup[o.region_id!]?.name,
  }))

  downloadFns[fileType](enriched, filename)
}

export const createCountyRegionSuffix = (filters: Filters) =>
  filters.country
    ? "_" + filters.country.name
    : filters.region
      ? "_" + filters.region.name
      : ""

export const createFilename = (
  model: Model,
  tabId: string | undefined,
  filters: Filters,
) =>
  new Date().toISOString().slice(0, 10) +
  `_${model}s` +
  (tabId ? "_" + tabId : "") +
  createCountyRegionSuffix(filters)
