import { error } from "@sveltejs/kit"

import type { DealHull } from "$lib/types/newtypes"

import type { PageLoad } from "./$types"

export const ssr = false

export const load: PageLoad = async ({ fetch, params }) => {
  const [dealID, dealVersion] = params.IDs.split("/").map(x => (x ? +x : undefined))

  if (!dealID) throw error(404, "Deal not found")

  const url = dealVersion
    ? `/api/deals/${dealID}/${dealVersion}/`
    : `/api/deals/${dealID}/`
  const ret = await fetch(url)
  const deal: DealHull = await ret.json()
  //
  // if (res.error) {
  //   if (res.error.graphQLErrors.map(e => e.message).includes("DEAL_NOT_FOUND"))
  //     throw error(404, "Deal not found")
  //   if (res.error.graphQLErrors.map(e => e.message).includes("MISSING_AUTHORIZATION"))
  //     throw error(401, "Unauthorized")
  //   throw error(500, `${res.error}`)
  // }
  // if (!res.data) throw error(500, `Unknown Problem: ${error}`)
  //
  // if (!res.data.deal) throw error(404, "Deal not found")
  // if (res.data.deal.status === Status.DRAFT && !dealVersion) {
  //   const dealV = res.data.deal.versions?.[0]?.id
  //   throw redirect(301, `/deal/${dealID}/${dealV}`)
  // }
  // // redirect if version is active version
  // const activeVersion = findActiveVersion(res.data.deal, "deal")
  // if (dealVersion && dealVersion === activeVersion?.id) {
  //   throw redirect(301, `/deal/${dealID}`)
  // }
  return { deal, dealID, dealVersion }
}
