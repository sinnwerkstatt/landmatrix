import { error, redirect } from "@sveltejs/kit"

import type { InvestorHull } from "$lib/types/data"

import type { InvestorSection } from "$components/Data/Investor/Sections/constants"

import type { LayoutLoad } from "./$types"

export const load: LayoutLoad = async ({ fetch, params, depends, parent }) => {
  depends("investor:detail")

  const { apiClient } = await parent()

  const investorID = parseInt(params.id)
  const investorVersion = parseInt(params.versionId ?? "")
  const investorSection = params.section as InvestorSection

  const baseUrl = investorVersion
    ? `/investor/${investorID}/${investorVersion}`
    : `/investor/${investorID}`

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

  if (investorVersion && investorVersion === investor.active_version_id) {
    console.warn("redirecting to active version")
    redirect(307, `/investor/${investorID}/`)
  }

  if (!investorVersion && !investor.active_version_id) {
    console.warn("redirecting to draft version")
    redirect(307, `/investor/${investorID}/${investor.draft_version_id}/`)
  }

  return {
    investor,
    investorID,
    investorVersion,
    investorSection,
    baseUrl,
  }
}
