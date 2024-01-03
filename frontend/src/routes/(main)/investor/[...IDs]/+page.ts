import { error } from "@sveltejs/kit"

import type { InvestorHull } from "$lib/types/newtypes"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ depends, params, fetch }) => {
  depends("investor:detail")

  const [investorID, investorVersion] = params.IDs.split("/").map(x =>
    x ? +x : undefined,
  )

  if (!investorID) throw error(404, "Investor not found")

  const url = investorVersion
    ? `/api/investors/${investorID}/${investorVersion}/`
    : `/api/investors/${investorID}/`
  const ret = await fetch(url)
  const investor: InvestorHull = await ret.json()

  // if (res.error) {
  //   if (res.error.graphQLErrors.map(e => e.message).includes("INVESTOR_NOT_FOUND"))
  //     throw error(404, "Investor not found")
  //   if (res.error.graphQLErrors.map(e => e.message).includes("MISSING_AUTHORIZATION"))
  //     throw error(401, "Unauthorized")
  //   throw error(500, `${res.error}`)
  // }
  // if (!res.data) throw error(500, `Unknown Problem: ${error}`)
  //
  // if (!res.data?.investor) throw error(404, "Investor not found")
  // if (res.data.investor.status === Status.DRAFT && !investorVersion) {
  //   const investorVersion = res.data.investor.versions?.[0]?.id
  //   throw redirect(301, `/investor/${investorID}/${investorVersion}`)
  // }
  // // redirect if version is active version
  // const activeVersion = findActiveVersion(res.data.investor, "investor")
  // if (investorVersion && investorVersion === activeVersion?.id) {
  //   throw redirect(301, `/investor/${investorID}`)
  // }
  return { investor: investor, investorID, investorVersion }
}
