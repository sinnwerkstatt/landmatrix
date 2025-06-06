import { stringify as csvStringify } from "csv-stringify/browser/esm/sync"
import { get } from "svelte/store"
import * as xlsx from "xlsx"

import { page } from "$app/state"

import { allUsers } from "$lib/stores"
import type { DealHull, InvestorHull } from "$lib/types/data"
import { aDownload } from "$lib/utils/download"

const COMMON_OBJ_COLUMNS = [
  "status",
  "first_created_at",
  "first_created_by",
  { key: "selected_version.modified_at", header: "modified_at" },
  "modified_by",
]
const INVESTOR_COLUMNS = [
  "id",
  { key: "selected_version.name", header: "name" },
  { key: "country_name", header: "country of origin" },
  // { key: "deals.length", header: "number of deals" }, seems unused
  ...COMMON_OBJ_COLUMNS,
]
const DEAL_COLUMNS = [
  "id",
  { key: "country_name", header: "target country" },
  { key: "selected_version.deal_size", header: "deal size" },
  {
    key: "selected_version.current_intention_of_investment",
    header: "current intention of investment",
  },
  "fully_updated_at",
  ...COMMON_OBJ_COLUMNS,
]

type SimpleObject = DealHull | InvestorHull
type EnrichedObject = Omit<SimpleObject, "first_created_by"> & {
  country_name?: string
  first_created_by?: string
  modified_by?: string
}

const toCSVString = (objects: EnrichedObject[], model: "deal" | "investor"): string =>
  csvStringify(objects, {
    header: true,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    columns: (model === "deal" ? DEAL_COLUMNS : INVESTOR_COLUMNS) as any,
  })

const _enrichObjects = (objects: SimpleObject[]): EnrichedObject[] =>
  objects.map(o => {
    const country = page.data.countries.find(
      c =>
        c.id ===
        ((o as DealHull).country_id ?? (o as InvestorHull).selected_version.country_id),
    )
    const country_name = country ? country.name : undefined

    const first_created_by =
      get(allUsers).find(u => u.id === o.first_created_by_id)?.username ?? undefined
    const modified_by =
      get(allUsers).find(u => u.id === o.selected_version.modified_by_id)?.username ??
      undefined

    return { ...o, country_name, first_created_by, modified_by }
  })

export const downloadAsCSV = (
  objects: SimpleObject[],
  model: "deal" | "investor",
  action: string,
) => {
  const csvString = toCSVString(_enrichObjects(objects), model)
  const blob = new Blob([csvString], { type: "text/csv" })
  aDownload(blob, `${action}_${model}.csv`)
}

export const downloadAsXLSX = (
  objects: SimpleObject[],
  model: "deal" | "investor",
  action: string,
) => {
  const csvString = toCSVString(_enrichObjects(objects), model)
  const wb = xlsx.read(csvString, { type: "string" })
  const data = xlsx.write(wb, { type: "array", bookType: "xlsx" })

  const blob = new Blob([data], {
    type: "application/ms-excel",
  })
  aDownload(blob, `${action}_${model}.xlsx`)
}
