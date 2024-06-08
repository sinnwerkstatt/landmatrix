import { error, redirect } from "@sveltejs/kit"

import type { DealHull } from "$lib/types/newtypes"

import type { DealSection } from "$components/Data/Deal/Sections/constants"

import type { LayoutLoad } from "./$types"
import { mutableDeal } from "./store"

export const load: LayoutLoad = async ({ params, fetch, parent, depends }) => {
  depends("deal:detail")

  const { user } = await parent()
  if (!user) error(403, "Permission denied")

  const dealID = parseInt(params.id)
  const dealVersion = params.versionId ? parseInt(params.versionId) : undefined

  const url = dealVersion
    ? `/api/deals/${dealID}/${dealVersion}/`
    : `/api/deals/${dealID}/`

  const ret = await fetch(url)

  if (ret.status === 404)
    error(404, dealVersion ? "Deal version not found" : "Deal not found")

  if (!ret.ok) error(ret.status, (await ret.json()).detail)

  const deal: DealHull = await ret.json()

  mutableDeal.set(structuredClone(deal))
  const originalDeal = JSON.stringify(deal)

  // TODO: @nuts are these still needed??
  // don't allow editing of older versions

  if (dealVersion && dealVersion !== deal.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(301, `/deal/edit/${dealID}/${deal.draft_version_id}/`)
  }

  // don't allow editing version of active deal
  if (dealVersion && dealVersion === deal.active_version_id) {
    console.warn("redirecting to active version")
    redirect(301, `/deal/edit/${dealID}/`)
  }

  // don't allow editing active deal if there are newer version
  if (!dealVersion && deal.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(301, `/deal/edit/${dealID}/${deal.draft_version_id}/`)
  }

  const baseUrl = dealVersion
    ? `/deal/edit/${dealID}/${dealVersion}`
    : `/deal/edit/${dealID}`

  return {
    deal,
    dealID,
    dealVersion,
    originalDeal,
    baseUrl,
    section: params.section as DealSection,
  }
}
