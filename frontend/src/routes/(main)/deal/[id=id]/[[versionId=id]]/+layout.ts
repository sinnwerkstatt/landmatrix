import { error, redirect } from "@sveltejs/kit"

import type { DealHull } from "$lib/types/newtypes"

import type { LayoutLoad } from "./$types"

export const load: LayoutLoad = async ({ fetch, params, depends }) => {
  depends("deal:detail")

  const dealID = parseInt(params.id)
  const dealVersion = params.versionId ? parseInt(params.versionId) : undefined

  const url = dealVersion
    ? `/api/deals/${dealID}/${dealVersion}/`
    : `/api/deals/${dealID}/`
  const ret = await fetch(url)

  if (!ret.ok) error(ret.status, (await ret.json()).detail)

  const deal: DealHull = await ret.json()

  if (deal.active_version_id === dealVersion) redirect(301, `/deal/${dealID}/`)

  if (!deal.active_version_id && !dealVersion) {
    redirect(301, `/deal/${dealID}/${deal.draft_version_id}/`)
  }

  return { deal, dealID, dealVersion }
}
