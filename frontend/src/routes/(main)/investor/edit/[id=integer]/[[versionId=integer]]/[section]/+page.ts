import { redirect } from "@sveltejs/kit"

import {
  INVESTOR_EDIT_SECTIONS,
  type InvestorEditSection,
} from "$components/Data/Investor/Sections/constants"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ params, url }) => {
  if (!INVESTOR_EDIT_SECTIONS.includes(params.section as InvestorEditSection)) {
    redirect(307, new URL("../general", url))
  }
}
