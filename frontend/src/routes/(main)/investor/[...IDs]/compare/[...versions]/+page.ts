import { error } from "@sveltejs/kit"
import { diff } from "deep-object-diff"

import type { InvestorHull } from "$lib/types/newtypes"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, fetch }) => {
  const [investorID] = params.IDs.split("/").map(x => (x ? +x : undefined))
  if (!investorID) error(404, "Investor not found")

  const [versionFrom, versionTo] = params.versions
    .split("/")
    .map(x => (x ? +x : undefined))

  if (!versionFrom || !versionTo) error(500, "insufficient parameters")

  const resFrom = await fetch(`/api/investors/${investorID}/${versionFrom}/`)
  const investorFrom: InvestorHull = await resFrom.json()
  const fromVersion = investorFrom.selected_version

  const resTo = await fetch(`/api/investors/${investorID}/${versionTo}/`)
  const investorTo: InvestorHull = await resTo.json()
  const toVersion = investorTo.selected_version

  if (!investorFrom || !investorTo) error(500, "problem")

  const investordiffy = Object.keys(diff(fromVersion, toVersion))

  return {
    investorID,
    fromVersion,
    toVersion,
    investordiff: investordiffy.length ? new Set(investordiffy) : new Set(),
    // datasourcesdiff: dsdiffy.length ? new Set(dsdiffy) : null,
    // involvementsdiff: idiffy.length ? new Set(idiffy) : null,
  }
}
