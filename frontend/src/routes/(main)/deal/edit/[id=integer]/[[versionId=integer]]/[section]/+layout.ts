import { error, redirect } from "@sveltejs/kit"

import type { DealHull } from "$lib/types/data"

import type { DealSection } from "$components/Data/Deal/Sections/constants"

import type { LayoutLoad } from "./$types"

export const load: LayoutLoad = async ({ params, fetch, parent, depends }) => {
  depends("deal:detail")

  const { user, apiClient } = await parent()
  if (!user) {
    error(403, "Permission denied")
  }

  const dealID = parseInt(params.id)
  const dealVersion = parseInt(params.versionId ?? "")
  const dealSection = params.section as DealSection

  const baseUrl = dealVersion
    ? `/deal/edit/${dealID}/${dealVersion}`
    : `/deal/edit/${dealID}`

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

  // don't allow editing of older versions
  if (dealVersion && dealVersion !== deal.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(307, `/deal/edit/${dealID}/${deal.draft_version_id}/`)
  }

  // don't allow editing version of active deal
  if (dealVersion && dealVersion === deal.active_version_id) {
    console.warn("redirecting to active version")
    redirect(307, `/deal/edit/${dealID}/`)
  }

  // don't allow editing active deal if there are newer version
  if (!dealVersion && deal.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(307, `/deal/edit/${dealID}/${deal.draft_version_id}/`)
  }

  return {
    deal,
    dealID,
    dealVersion,
    dealSection,
    baseUrl,
  }
}
