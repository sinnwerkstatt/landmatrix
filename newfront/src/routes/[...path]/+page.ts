import { pageQuery } from "$lib/queries"
import type { WagtailPage } from "$lib/types/wagtail"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ url, fetch }) => {
  const page: WagtailPage = await pageQuery(url, fetch)
  return { page }
}
