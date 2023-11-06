import type { ComponentType } from "svelte"
import { error } from "@sveltejs/kit"

import LACP from "$components/Data/Charts/CountryProfile/LACP.svelte"
import LSLAByNegotiation from "$components/Data/Charts/CountryProfile/LSLAByNegotiation.svelte"
import DynamicsOfDeal from "$components/Data/Charts/CountryProfile/DynamicsOfDeal.svelte"
import IntentionsPerCategory from "$components/Data/Charts/CountryProfile/IntentionsPerCategory.svelte"
import ConcludedDealsOverTime from "$components/Data/Charts/CountryProfile/ConcludedDealsOverTime.svelte"

import type { PageLoad } from "./$types"

export const ssr = false

const stripTrailingSlash = (path: string): string =>
  path.endsWith("/") ? path.slice(0, -1) : path

const countryProfiles: {
  key: string
  component: ComponentType
}[] = [
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
]

export const load: PageLoad = async ({ params }) => {
  const stripped = stripTrailingSlash(params.path)
  const profile = countryProfiles.find(profile => profile.key === stripped)
  if (!profile) {
    throw error(404, "Page not found")
  }
  return { profile }
}
