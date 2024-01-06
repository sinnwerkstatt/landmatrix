import { error } from "@sveltejs/kit"
import { diff } from "deep-object-diff"

import { dealQuery } from "$lib/dealQueries"
import type { Deal } from "$lib/types/deal"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, parent }) => {
  const { urqlClient } = await parent()
  const [dealID] = params.IDs.split("/").map(x => (x ? +x : undefined))
  if (!dealID) error(404, `Deal not found`)

  const [versionFrom, versionTo] = params.versions
    .split("/")
    .map(x => (x ? +x : undefined))

  if (!versionFrom || !versionTo) error(500, "insufficient parameters")

  const vFrom = await urqlClient
    .query<{ deal: Deal }>(
      dealQuery,
      { id: dealID, version: versionFrom },
      { requestPolicy: "network-only" },
    )
    .toPromise()
  const dealFrom = vFrom.data?.deal
  const vTo = await urqlClient
    .query<{ deal: Deal }>(
      dealQuery,
      { id: dealID, version: versionTo },
      { requestPolicy: "network-only" },
    )
    .toPromise()
  const dealTo = vTo.data?.deal

  if (!dealFrom || !dealTo) error(500, "problem")

  const dealdiffy = Object.keys(diff(dealFrom, dealTo))
  const locdiffy = Object.keys(diff(dealFrom.locations, dealTo.locations))
  const dsdiffy = Object.keys(diff(dealFrom.datasources, dealTo.datasources))
  const condiffy = Object.keys(diff(dealFrom.contracts, dealTo.contracts))

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
