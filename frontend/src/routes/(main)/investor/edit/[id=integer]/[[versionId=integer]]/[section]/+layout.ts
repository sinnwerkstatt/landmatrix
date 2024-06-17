import { error, redirect } from "@sveltejs/kit"

import type { InvestorHull } from "$lib/types/data"

import type { InvestorEditSection } from "$components/Data/Investor/Sections/constants"

import type { LayoutLoad } from "./$types"

// Duplicate lines between display and edit views as well as
// between deal and investor load functions
// TODO: Refactor
// Ideas:
// - reusable load functions
// - restructure routes to /[obj]/[id]/[[vId]]/[[edit]]
export const load: LayoutLoad = async ({ params, url, fetch, parent, depends }) => {
  depends("investor:detail")

  const { user, apiClient } = await parent()
  if (!user) {
    error(403, "Permission denied")
  }

  const investorID = parseInt(params.id)
  const investorVersion = parseInt(params.versionId ?? "")
  const investorSection = params.section as InvestorEditSection

  const baseUrl = investorVersion
    ? `/investor/edit/${investorID}/${investorVersion}`
    : `/investor/edit/${investorID}`

  const ret = investorVersion
    ? await apiClient.GET("/api/investors/{id}/{version_id}/", {
        params: { path: { id: investorID, version_id: investorVersion } },
        fetch,
      })
    : await apiClient.GET("/api/investors/{id}/", {
        params: { path: { id: investorID } },
        fetch,
      })

  if (ret.error) {
    // @ts-expect-error openapi-fetch types broken
    error(ret.response.status, ret.error.detail)
  }

  // FIXME: Overwrite with patched InvestorHull
  const investor = ret.data as unknown as InvestorHull

  // don't allow editing of older versions
  if (investorVersion && investorVersion !== investor.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(307, `/investor/edit/${investorID}/${investor.draft_version_id}/`)
  }

  // don't allow editing version of active investor
  if (investorVersion && investorVersion === investor.active_version_id) {
    console.warn("redirecting to active version")
    redirect(307, `/investor/edit/${investorID}/`)
  }

  // don't allow editing active investor if there are newer version
  if (!investorVersion && investor.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(307, `/investor/edit/${investorID}/${investor.draft_version_id}/`)
  }

  return {
    investor,
    investorID,
    investorVersion,
    investorSection,
    baseUrl,
  }
}
