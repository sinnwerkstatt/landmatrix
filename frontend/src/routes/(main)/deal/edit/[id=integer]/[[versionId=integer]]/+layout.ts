import { error, redirect } from "@sveltejs/kit"

import type { DealHull, MutableDealHull } from "$lib/types/data"

import { mutableDeal } from "$components/Data/stores"

import type { LayoutLoad } from "./$types"

export const load: LayoutLoad = async ({ params, parent, depends }) => {
  depends("deal:detail")

  const { user, apiClient } = await parent()
  if (!user) {
    error(403, "Permission denied")
  }

  const dealID = parseInt(params.id)
  const dealVersion = params.versionId ? parseInt(params.versionId) : null

  const baseUrl = dealVersion
    ? `/deal/edit/${dealID}/${dealVersion}`
    : `/deal/edit/${dealID}`

  const ret = dealVersion
    ? await apiClient.GET("/api/deals/{id}/{version_id}/", {
        params: { path: { id: dealID, version_id: dealVersion } },
      })
    : await apiClient.GET("/api/deals/{id}/", {
        params: { path: { id: dealID } },
      })

  if (ret.error) {
    // @ts-expect-error openapi-fetch types broken
    error(ret.response.status, ret.error.detail)
  }

  // FIXME: Overwrite with patched DealHull
  const deal = ret.data as unknown as DealHull

  // don't allow editing of older versions
  if (dealVersion && dealVersion !== deal.draft_version_id) {
    const url = `/deal/edit/${dealID}/${deal.draft_version_id}/`
    console.warn(`redirecting to draft version: ${url}`)
    redirect(307, url)
  }

  // don't allow editing version of active deal
  if (dealVersion && dealVersion === deal.active_version_id) {
    const url = `/deal/edit/${dealID}/`
    console.warn(`redirecting to active version: ${url}`)
    redirect(307, url)
  }

  // don't allow editing active deal if there are newer version
  if (!dealVersion && deal.draft_version_id) {
    const url = `/deal/edit/${dealID}/${deal.draft_version_id}/`
    console.warn(`redirecting to draft version: ${url}`)
    redirect(307, url)
  }

  mutableDeal.set(structuredClone(deal) as MutableDealHull)

  return {
    deal,
    dealID,
    dealVersion,
    baseUrl,
  }
}
