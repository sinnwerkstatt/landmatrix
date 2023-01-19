import { error } from "@sveltejs/kit"
import { diff } from "deep-object-diff"

import { investor_gql_query } from "$lib/investor_queries"
import type { Investor } from "$lib/types/investor"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, parent }) => {
  const { urqlClient } = await parent()
  const [investorID] = params.IDs.split("/").map(x => (x ? +x : undefined))
  if (!investorID) throw error(404, "Investor not found")

  const [versionFrom, versionTo] = params.versions
    .split("/")
    .map(x => (x ? +x : undefined))

  if (!versionFrom || !versionTo) throw error(500, "insufficient parameters")

  const vFrom = await urqlClient
    .query(
      investor_gql_query,
      { id: investorID, version: versionFrom, includeDeals: false },
      { requestPolicy: "network-only" },
    )
    .toPromise()
  const investorFrom: Investor = vFrom.data.investor
  const vTo = await urqlClient
    .query(
      investor_gql_query,
      { id: investorID, version: versionTo, includeDeals: false },
      { requestPolicy: "network-only" },
    )
    .toPromise()
  const investorTo: Investor = vTo.data.investor

  const investordiffy = Object.keys(diff(investorFrom, investorTo))
  const dsdiffy = Object.keys(diff(investorFrom.datasources, investorTo.datasources))
  const idiffy = Object.keys(diff(investorFrom.investors, investorTo.investors))

  return {
    investorID,
    versionFrom,
    versionTo,
    investorFrom,
    investorTo,
    investordiff: investordiffy.length ? new Set(investordiffy) : new Set(),
    datasourcesdiff: dsdiffy.length ? new Set(dsdiffy) : null,
    involvementsdiff: idiffy.length ? new Set(idiffy) : null,
  }
}
