import { redirect } from "@sveltejs/kit"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ parent }) => {
  const data = await parent()

  const path = data.dealVersion
    ? `/deal/edit/${data.dealID}/${data.dealVersion}/`
    : `/deal/edit/${data.dealID}/`

  throw redirect(307, path + "locations")
  // throw error(404)

  // TODO: write matcher : https://kit.svelte.dev/docs/advanced-routing#matching
}
