import { error, redirect } from "@sveltejs/kit"

import type { InvestorHull } from "$lib/types/data"

import type { PageLoad } from "./$types"

export const ssr = false

export const load: PageLoad = async ({ depends, params, parent }) => {
  depends("investor:detail")

  const { user } = await parent()
  if (!user) error(403, "Permission denied")

  const investorID = parseInt(params.id)
  const versionID = params.versionId ? parseInt(params.versionId) : undefined

  if (!investorID) redirect(301, "/list/investors/")

  const ret = await fetch(
    versionID
      ? `/api/investors/${investorID}/${versionID}/`
      : `/api/investors/${investorID}/`,
  )

  if (ret.status === 404)
    error(404, versionID ? "Investor version not found" : "Investor not found")

  if (!ret.ok) error(ret.status, (await ret.json()).detail)

  const investor: InvestorHull = await ret.json()

  // don't allow editing of older versions
  if (versionID && versionID !== investor.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(301, `/investor/edit/${investorID}/${investor.draft_version_id}/`)
  }

  // don't allow editing version of active investor
  if (versionID && versionID === investor.active_version_id) {
    console.warn("redirecting to active version")
    redirect(301, `/investor/edit/${investorID}/`)
  }

  // don't allow editing active investor if there are newer version
  if (!versionID && investor.draft_version_id) {
    console.warn("redirecting to draft version")
    redirect(301, `/investor/edit/${investorID}/${investor.draft_version_id}/`)
  }

  const originalInvestor = JSON.stringify(investor)
  return { investor, investorID, versionID, originalInvestor }
}
