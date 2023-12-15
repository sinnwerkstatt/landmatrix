import { error, redirect } from "@sveltejs/kit"

import type { DealHull } from "$lib/types/newtypes"

import type { PageLoad } from "./$types"

export const ssr = false

export const load: PageLoad = async ({ fetch, params, depends }) => {
  depends("deal:detail")
  const [dealID, dealVersion] = params.IDs.split("/").map(x => (x ? +x : undefined))

  if (!dealID) throw error(404, "Deal not found")

  const url = dealVersion
    ? `/api/deals/${dealID}/${dealVersion}/`
    : `/api/deals/${dealID}/`
  const ret = await fetch(url)

  if (!ret.ok) throw error(ret.status, (await ret.json()).detail)

  const deal: DealHull = await ret.json()

  if (deal.active_version === dealVersion) throw redirect(301, `/deal/${dealID}/`)

  //  TODO this block
  // if (res.data.deal.status === Status.DRAFT && !dealVersion) {
  //   const dealV = res.data.deal.versions?.[0]?.id
  //   throw redirect(301, `/deal/${dealID}/${dealV}`)
  // }
  // // redirect if version is active version

  return { deal, dealID, dealVersion }
}
