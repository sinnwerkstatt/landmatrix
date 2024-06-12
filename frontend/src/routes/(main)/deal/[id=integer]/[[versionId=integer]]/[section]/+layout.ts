import { error, redirect } from "@sveltejs/kit"

import type { DealSection } from "$components/Data/Deal/Sections/constants"

import type { LayoutLoad } from "./$types"

export const load: LayoutLoad = async ({ fetch, params, depends, parent }) => {
  depends("deal:detail")

  const { apiClient } = await parent()

  const dealID = parseInt(params.id)
  const dealVersion = parseInt(params.versionId as string)
  const dealSection = params.section as DealSection

  const baseUrl = dealVersion ? `/deal/${dealID}/${dealVersion}` : `/deal/${dealID}`

  const ret = dealVersion
    ? await apiClient.GET("/api/deals/{id}/{version_id}/", {
        // TODO: deal_version should be number in schema
        params: { path: { id: dealID, version_id: `${dealVersion}` } },
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

  const deal = ret.data

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
