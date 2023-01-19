import { pageQuery } from "$lib/queries"
import type { BlogPage } from "$lib/types/wagtail"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ url, fetch }) => {
  const page: BlogPage = await pageQuery(url, fetch)

  return { page }
}
