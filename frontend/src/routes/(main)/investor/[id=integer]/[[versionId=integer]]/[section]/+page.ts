import { redirect } from "@sveltejs/kit"

import {
  INVESTOR_SECTIONS,
  type InvestorSection,
} from "$components/Data/Investor/Sections/constants"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, url }) => {
  if (!INVESTOR_SECTIONS.includes(params.section as InvestorSection)) {
    redirect(307, new URL("../general", url))
  }
}
