import { error, redirect } from "@sveltejs/kit"

import type { InvestorHull } from "$lib/types/newtypes"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ depends, params, fetch }) => {
  depends("investor:detail")

  const [investorID, investorVersion] = params.IDs.split("/").map(x =>
    x ? +x : undefined,
  )

  if (!investorID) error(404, "Investor not found")

  const url = investorVersion
    ? `/api/investors/${investorID}/${investorVersion}/`
    : `/api/investors/${investorID}/`
  const ret = await fetch(url)

  if (!ret.ok) error(ret.status, (await ret.json()).detail)

  const investor: InvestorHull = await ret.json()

  if (investor.active_version_id === investorVersion)
    redirect(301, `/investor/${investorID}/`)

  if (!investor.active_version_id && !investorVersion) {
    redirect(301, `/investor/${investorID}/${investor.draft_version_id}/`)
  }

  return { investor: investor, investorID, investorVersion }
}
