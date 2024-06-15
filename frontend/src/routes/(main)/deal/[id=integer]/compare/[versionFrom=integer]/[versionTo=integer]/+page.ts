import { error } from "@sveltejs/kit"
import { diff } from "deep-object-diff"

import type { DealHull } from "$lib/types/data"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, fetch }) => {
  const dealID = parseInt(params.id)

  const resFrom = await fetch(`/api/deals/${dealID}/${params.versionFrom}/`)
  const dealFrom: DealHull = await resFrom.json()
  const fromVersion = dealFrom.selected_version
  const resTo = await fetch(`/api/deals/${dealID}/${params.versionTo}/`)
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
