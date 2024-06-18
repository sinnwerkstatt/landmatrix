import { error, redirect } from "@sveltejs/kit"

import type { DealHull } from "$lib/types/data"

import type { DealSection } from "$components/Data/Deal/Sections/constants"

import type { LayoutLoad } from "./$types"

export const load: LayoutLoad = async ({ fetch, params, depends, parent }) => {
  depends("deal:detail")

  const { apiClient } = await parent()

  const dealID = parseInt(params.id)
  const dealVersion = parseInt(params.versionId ?? "")
  const dealSection = params.section as DealSection

  const baseUrl = dealVersion ? `/deal/${dealID}/${dealVersion}` : `/deal/${dealID}`

  const ret = dealVersion
    ? await apiClient.GET("/api/deals/{id}/{version_id}/", {
        params: { path: { id: dealID, version_id: dealVersion } },
        fetch,
      })
    : await apiClient.GET("/api/deals/{id}/", {
        params: { path: { id: dealID } },
        fetch,
      })

  if (ret.error) {
    // @ts-expect-error openapi-fetch types broken
    error(ret.response.status, ret.error.detail)
  }

  // FIXME: Overwrite with patched DealHull
  const deal = ret.data as unknown as DealHull

  if (dealVersion && dealVersion === deal.active_version_id) {
    console.warn("redirecting to active version")
    redirect(307, `/deal/${dealID}/`)
  }

  if (!dealVersion && !deal.active_version_id) {
    console.warn("redirecting to draft version")
    redirect(307, `/deal/${dealID}/${deal.draft_version_id}/`)
  }

  return {
    deal,
    dealID,
    dealVersion,
    dealSection,
    baseUrl,
  }
}
