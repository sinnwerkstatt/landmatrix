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
  const fromVersion = dealFrom.selected_version
  const resTo = await fetch(`/api/deals/${dealID}/${versionTo}/`)
  const dealTo: DealHull = await resTo.json()
  const toVersion = dealTo.selected_version
  if (!dealFrom || !dealTo) error(500, "problem")

  const dealdiffy = Object.keys(diff(fromVersion, toVersion))

  return {
    dealID,
    fromVersion,
    toVersion,
    dealdiff: dealdiffy.length ? new Set(dealdiffy) : new Set(),
  }
}
