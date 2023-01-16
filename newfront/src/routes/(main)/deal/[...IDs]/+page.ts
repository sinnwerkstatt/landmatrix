import { error, redirect } from "@sveltejs/kit"

import { deal_gql_query } from "$lib/deal_queries"
import { findActiveVersion } from "$lib/helpers"
import type { Deal } from "$lib/types/deal"
import { Status } from "$lib/types/generics"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, parent }) => {
  const { urqlClient } = await parent()
  const [dealID, dealVersion] = params.IDs.split("/").map(x => (x ? +x : undefined))

  if (!dealID) throw error(404, "Deal not found")

  const res = await urqlClient
    .query<{ deal: Deal }>(deal_gql_query, { id: dealID, version: dealVersion })
    .toPromise()
  if (res.error) {
    if (res.error.graphQLErrors[0].message === "DEAL_NOT_FOUND")
      throw error(404, "Deal not found")
    if (res.error.graphQLErrors[0].message === "MISSING_AUTHORIZATION")
      throw error(401, "Unauthorized")
    throw error(500, `${res.error}`)
  }
  if (!res.data) throw error(500, `Unknown Problem: ${error}`)

  if (!res.data.deal) throw error(404, "Deal not found")
  if (res.data.deal.status === Status.DRAFT && !dealVersion) {
    const dealV = res.data.deal.versions?.[0]?.id
    throw redirect(301, `/deal/${dealID}/${dealV}`)
  }
  // redirect if version is active version
  const activeVersion = findActiveVersion(res.data.deal, "deal")
  if (dealVersion && dealVersion === activeVersion?.id) {
    throw redirect(301, `/deal/${dealID}`)
  }
  return { deal: res.data.deal, dealID, dealVersion }
}
