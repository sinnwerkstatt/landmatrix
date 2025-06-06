import { error } from "@sveltejs/kit"
import type { Component } from "svelte"

import ConcludedDealsOverTime from "$components/Data/Charts/CountryProfile/ConcludedDealsOverTime.svelte"
import DynamicsOfDeal from "$components/Data/Charts/CountryProfile/DynamicsOfDeal.svelte"
import IntentionsPerCategory from "$components/Data/Charts/CountryProfile/IntentionsPerCategory.svelte"
import LACP from "$components/Data/Charts/CountryProfile/LACP.svelte"
import LSLAByNegotiation from "$components/Data/Charts/CountryProfile/LSLAByNegotiation.svelte"

import type { PageLoad } from "./$types"

export const ssr = false

const stripTrailingSlash = (path: string): string =>
  path.endsWith("/") ? path.slice(0, -1) : path

interface CountryProfile {
  key: string
  component: Component
}

const countryProfiles = [
  {
    key: "land-acquisitions",
    component: LACP,
  },
  {
    key: "lsla",
    component: LSLAByNegotiation,
  },
  {
    key: "dynamics-of-deal",
    component: DynamicsOfDeal,
  },
  {
    key: "intentions-of-investments",
    component: IntentionsPerCategory,
  },
  {
    key: "concluded-deals-over-time",
    component: ConcludedDealsOverTime,
  },
] as const satisfies CountryProfile[]

export const load: PageLoad = async ({ params }) => {
  const stripped = stripTrailingSlash(params.path)
  const profile = countryProfiles.find(profile => profile.key === stripped)
  if (!profile) {
    error(404, "Page not found")
  }
  return { profile }
}
