import { redirect } from "@sveltejs/kit"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ parent }) => {
  const data = await parent()

  const path = data.dealVersion
    ? `/deal/edit/${data.dealID}/${data.dealVersion}/`
    : `/deal/edit/${data.dealID}/`

  redirect(301, path + "locations/")
}
