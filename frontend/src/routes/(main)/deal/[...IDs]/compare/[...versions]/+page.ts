import { error } from "@sveltejs/kit"
import { diff } from "deep-object-diff"

import type { DealHull } from "$lib/types/newtypes"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, fetch }) => {
  const [dealID] = params.IDs.split("/").map(x => (x ? +x : undefined))
  if (!dealID) error(404, `Deal not found`)

  const [versionFrom, versionTo] = params.versions
    .split("/")
    .map(x => (x ? +x : undefined))

  if (!versionFrom || !versionTo) error(500, "insufficient parameters")

  const resFrom = await fetch(`/api/deals/${dealID}/${versionFrom}/`)
  const dealFrom: DealHull = await resFrom.json()
  const resTo = await fetch(`/api/deals/${dealID}/${versionTo}/`)
  const dealTo: DealHull = await resTo.json()

  if (!dealFrom || !dealTo) error(500, "problem")

  const dealdiffy = Object.keys(
    diff(dealFrom.selected_version, dealTo.selected_version),
  )
  const locdiffy = Object.keys(
    diff(dealFrom.selected_version.locations, dealTo.selected_version.locations),
  )
  const dsdiffy = Object.keys(
    diff(dealFrom.selected_version.locations, dealTo.selected_version.locations),
  )
  const condiffy = Object.keys(
    diff(dealFrom.selected_version.datasources, dealTo.selected_version.datasources),
  )

  return {
    dealID,
    versionFrom,
    versionTo,
    dealFrom,
    dealTo,
    dealdiff: dealdiffy.length ? new Set(dealdiffy) : new Set(),
    locationsdiff: locdiffy.length ? new Set(locdiffy) : null,
    datasourcesdiff: dsdiffy.length ? new Set(dsdiffy) : null,
    contractsdiff: condiffy.length ? new Set(condiffy) : null,
  }
}
