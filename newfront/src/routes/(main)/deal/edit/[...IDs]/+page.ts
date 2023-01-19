import { error, redirect } from "@sveltejs/kit"

import { deal_gql_query } from "$lib/deal_queries"
import { findActiveVersion } from "$lib/helpers"
import type { Deal } from "$lib/types/deal"

import type { PageLoad } from "./$types"

export const ssr = false

export const load: PageLoad = async ({ params, parent }) => {
  const { user, urqlClient } = await parent()
  if (!user) throw error(403, "Permission denied")

  const [dealID, dealVersion] = params.IDs.split("/").map(x => (x ? +x : undefined))
  const { data } = await urqlClient
    .query<{ deal: Deal }>(deal_gql_query, { id: dealID, version: dealVersion })
    .toPromise()
  if (!data?.deal)
    throw error(404, dealVersion ? "Deal version not found" : "Deal not found")

  // don't allow editing of older versions -> redirect too current draft version
  const lastVersion = data.deal.versions[0]
  if (dealVersion && dealVersion !== lastVersion.id) {
    window.alert("redirecting to draft version")
    throw redirect(301, `/deal/edit/${dealID}/${lastVersion.id}`)
  }
  // don't allow editing version of active deal -> redirect to create new version
  const activeVersion = findActiveVersion(data.deal, "deal")
  if (dealVersion && dealVersion === activeVersion?.id) {
    window.alert("redirecting to active version")
    throw redirect(301, `/deal/edit/${dealID}`)
  }
  // don't allow editing active deal if there are newer version
  if (!dealVersion && lastVersion.id !== activeVersion?.id) {
    window.alert("redirecting to draft version")
    throw redirect(301, `/deal/edit/${dealID}/${lastVersion.id}`)
  }
  return { deal: data.deal, dealID, dealVersion }
}
