import { error, redirect, type NumericRange } from "@sveltejs/kit"

import type { InvestorHull } from "$lib/types/data"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ depends, params, fetch }) => {
  depends("investor:detail")

  const investorID = parseInt(params.id)
  const investorVersion = params.versionId ? parseInt(params.versionId) : undefined

  const url = investorVersion
    ? `/api/investors/${investorID}/${investorVersion}/`
    : `/api/investors/${investorID}/`
  const ret = await fetch(url)

  if (ret.status === 404)
    error(404, investorVersion ? "Investor version not found" : "Investor not found")

  if (!ret.ok) error(ret.status as NumericRange<400, 599>, (await ret.json()).detail)

  const investor: InvestorHull = await ret.json()

  if (investor.active_version_id === investorVersion) {
    redirect(301, `/investor/${investorID}/`)
  }

  if (!investor.active_version_id && !investorVersion) {
    redirect(301, `/investor/${investorID}/${investor.draft_version_id}/`)
  }

  return { investor: investor, investorID, investorVersion }
}
