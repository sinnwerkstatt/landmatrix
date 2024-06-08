import { error, redirect } from "@sveltejs/kit"

import type { DealHull } from "$lib/types/newtypes"

import type { DealSection } from "$components/Data/Deal/Sections/constants"

import type { LayoutLoad } from "./$types"

export const load: LayoutLoad = async ({ fetch, params, depends, parent }) => {
  depends("deal:detail")

  const dealID = parseInt(params.id)
  const dealVersion = params.versionId ? parseInt(params.versionId) : undefined

  const { apiClient } = await parent()

  const ret = dealVersion
    ? await apiClient.GET("/api/deals/{id}/{version_id}/", {
        // TODO: change dealVersion type to number
        params: { path: { id: dealID, version_id: `${dealVersion}` } },
        fetch,
      })
    : await apiClient.GET("/api/deals/{id}/", {
        params: { path: { id: dealID } },
        fetch,
      })

  if (ret.error) {
    if (ret.response.status === 404)
      error(404, dealVersion ? "Deal version not found" : "Deal not found")

    error(ret.response.status, ret.error.detail)
  }

  // TODO: FIXME
  const deal: DealHull = ret.data

  if (deal.active_version_id === dealVersion) {
    redirect(301, `/deal/${dealID}/`)
  }

  if (!deal.active_version_id && !dealVersion) {
    redirect(301, `/deal/${dealID}/${deal.draft_version_id}/`)
  }

  return { deal, dealID, dealVersion, section: params.section as DealSection }
}
