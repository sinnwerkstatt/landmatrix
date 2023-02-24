import { stringify } from "csv-stringify/browser/esm/sync"
import * as xlsx from "xlsx"

import type { Deal } from "$lib/types/deal"
import type { Investor } from "$lib/types/investor"

const COMMON_OBJ_COLUMNS = [
  "status",
  "draft_status",
  "created_at",
  "created_by.username",
  "modified_at",
  "modified_by.username",
]
const INVESTOR_COLUMNS = [
  "id",
  "name",
  { key: "country.name", header: "country of origin" },
  { key: "deals.length", header: "number of deals" },
  ...COMMON_OBJ_COLUMNS,
]
const DEAL_COLUMNS = [
  "id",
  { key: "country.name", header: "target country" },
  "deal_size",
  "fully_updated_at",
  ...COMMON_OBJ_COLUMNS,
]

const toCSVString = (
  objects: (Deal | Investor)[],
  model: "deal" | "investor",
): string =>
  stringify(objects, {
    header: true,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    columns: (model === "deal" ? DEAL_COLUMNS : INVESTOR_COLUMNS) as any,
  })

export const downloadAsCSV = (
  objects: (Deal | Investor)[],
  model: "deal" | "investor",
  action: string,
) => {
  const csvString = toCSVString(objects, model)
  const blob = new Blob([csvString], {
    type: "text/csv",
  })
  aDownload(blob, `${action}_${model}.csv`)
}

export const downloadAsXLSX = (
  objects: (Deal | Investor)[],
  model: "deal" | "investor",
  action: string,
) => {
  const csvString = toCSVString(objects, model)
  const wb = xlsx.read(csvString, { type: "string" })
  const data = xlsx.write(wb, { type: "array", bookType: "xlsx" })

  const blob = new Blob([data], {
    type: "application/ms-excel",
  })
  aDownload(blob, `${action}_${model}.xlsx`)
}

const aDownload = (blob: Blob, filename: string) => {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement("a")

  a.setAttribute("href", url)
  a.setAttribute("download", filename)
  a.click()
}
