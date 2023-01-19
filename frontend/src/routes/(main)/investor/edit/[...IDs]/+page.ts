import { error, redirect } from "@sveltejs/kit"

import { findActiveVersion } from "$lib/helpers"
import { investor_gql_query } from "$lib/investor_queries"
import type { Investor } from "$lib/types/investor"

import type { PageLoad } from "./$types"

// export const ssr = false

export const load: PageLoad = async ({ params, parent }) => {
  const { user, urqlClient } = await parent()
  if (!user) throw error(403, "Permission denied")

  const [investorID, investorVersion] = params.IDs.split("/").map(x =>
    x ? +x : undefined,
  )
  const { data } = await urqlClient
    .query<{ investor: Investor }>(investor_gql_query, {
      id: investorID,
      version: investorVersion,
      depth: 0,
      includeDeals: false,
    })
    .toPromise()
  if (!data?.investor)
    throw error(
      404,
      investorVersion ? "Investor version not found" : "Investor not found",
    )
  // don't allow editing of older versions -> redirect too current draft version
  const lastVersion = data.investor.versions[0]
  if (investorVersion && investorVersion !== lastVersion.id) {
    window.alert("redirecting to draft version")
    throw redirect(301, `/investor/edit/${investorID}/${lastVersion.id}`)
  }
  // don't allow editing version of active deal -> redirect to create new version
  const activeVersion = findActiveVersion(data.investor, "investor")
  if (investorVersion && investorVersion === activeVersion?.id) {
    window.alert("redirecting to active version")
    throw redirect(301, `/investor/edit/${investorID}`)
  }
  // don't allow editing active deal if there are newer version
  if (!investorVersion && lastVersion.id !== activeVersion?.id) {
    window.alert("redirecting to draft version")
    throw redirect(301, `/investor/edit/${investorID}/${lastVersion.id}`)
  }
  return { investor: data.investor, investorID, investorVersion }
}
