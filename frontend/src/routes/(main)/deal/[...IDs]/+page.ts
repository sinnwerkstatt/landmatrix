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

  if (deal.active_version_id === dealVersion) throw redirect(301, `/deal/${dealID}/`)

  if (!deal.active_version_id && !dealVersion) {
    throw redirect(301, `/deal/${dealID}/${deal.draft_version_id}/`)
  }

  return { deal, dealID, dealVersion }
}
