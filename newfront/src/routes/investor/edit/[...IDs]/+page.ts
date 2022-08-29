import { error } from "@sveltejs/kit"

import { investor_gql_query } from "$lib/investor_queries"
import type { Investor } from "$lib/types/investor"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, parent }) => {
  const { user, urqlClient } = await parent()
  if (!user) throw error(403, "Permission denied")

  const [investorID, investorVersion] = params.IDs.split("/").map(x =>
    x ? +x : undefined,
  )
  const { data } = await urqlClient
    .query<{ investor: Investor[] }>(investor_gql_query, {
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

  return { investor: data.investor, investorID, investorVersion }
}
