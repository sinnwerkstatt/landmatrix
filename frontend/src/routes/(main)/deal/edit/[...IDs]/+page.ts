import { error, redirect } from "@sveltejs/kit"

import type { DealHull } from "$lib/types/newtypes"

import type { PageLoad } from "./$types"

export const ssr = false

export const load: PageLoad = async ({ params, fetch, parent, depends }) => {
  depends("deal:detail")

  const { user } = await parent()
  if (!user) error(403, "Permission denied")

  const [dealID, versionID] = params.IDs.split("/").map(x => (x ? +x : undefined))

  if (!dealID) redirect(301, "/list/deals/")
  const ret = await fetch(
    versionID ? `/api/deals/${dealID}/${versionID}/` : `/api/deals/${dealID}/`,
  )

  if (ret.status === 404)
    error(404, versionID ? "Deal version not found" : "Deal not found")

  if (!ret.ok) error(ret.status, (await ret.json()).detail)

  const deal: DealHull = await ret.json()

  // don't allow editing of older versions
  if (versionID && versionID !== deal.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(301, `/deal/edit/${dealID}/${deal.draft_version_id}/`)
  }

  // don't allow editing version of active deal
  if (versionID && versionID === deal.active_version_id) {
    console.warn("redirecting to active version")
    redirect(301, `/deal/edit/${dealID}/`)
  }
  // don't allow editing active deal if there are newer version
  if (!versionID && deal.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(301, `/deal/edit/${dealID}/${deal.draft_version_id}/`)
  }

  const originalDeal = JSON.stringify(deal)
  return { deal, dealID, versionID, originalDeal }
}
