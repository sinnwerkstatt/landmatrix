import { error, redirect } from "@sveltejs/kit"

import { deal_gql_query } from "$lib/deal_queries"
import type { Deal } from "$lib/types/deal"

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
    throw error(500, `${res.error}`)
  }
  if (!res.data) throw error(500, `Unknown Problem: ${error}`)

  if (!res.data.deal) throw error(404, "Deal not found")
  if (res.data.deal.status === 1 && !dealVersion) {
    const dealV = res.data.deal.versions?.[0]?.id
    throw redirect(301, `/deal/${dealID}/${dealV}`)
  }
  return { deal: res.data.deal, dealID, dealVersion }
}
