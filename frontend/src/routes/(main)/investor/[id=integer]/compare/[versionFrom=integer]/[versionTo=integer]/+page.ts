import { error } from "@sveltejs/kit"
import { diff } from "deep-object-diff"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, parent }) => {
  const { apiClient } = await parent()

  const investorId = parseInt(params.id)
  const fromVersionId = parseInt(params.versionFrom)
  const toVersionId = parseInt(params.versionTo)

  const resFrom = await apiClient.GET("/api/investors/{id}/{version_id}/", {
    params: { path: { id: investorId, version_id: fromVersionId } },
  })

  if (resFrom.error) {
    // @ts-expect-error openapi-fetch types broken
    error(resFrom.response.status, resFrom.error.detail)
  }

  const resTo = await apiClient.GET("/api/investors/{id}/{version_id}/", {
    params: { path: { id: investorId, version_id: toVersionId } },
  })

  if (resTo.error) {
    // @ts-expect-error openapi-fetch types broken
    error(resTo.response.status, resTo.error.detail)
  }

  const fromVersion = resFrom.data.selected_version
  const toVersion = resTo.data.selected_version

  const investordiffy = Object.keys(diff(fromVersion, toVersion))

  return {
    investorId,
    fromVersion,
    toVersion,
    investordiff: new Set(investordiffy),
  }
}
