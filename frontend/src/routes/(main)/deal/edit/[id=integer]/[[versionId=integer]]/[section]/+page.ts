import { redirect } from "@sveltejs/kit"

import {
  DEAL_SECTIONS,
  type DealSection,
} from "$components/Data/Deal/Sections/constants"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, url }) => {
  const dealSection = params.section as DealSection

  if (!DEAL_SECTIONS.includes(dealSection)) {
    redirect(307, new URL("../locations", url))
  }

  return { dealSection }
}
