import { pageQuery } from "$lib/queries"
import type { BlogPage, WagtailPage } from "$lib/types/wagtail"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ url, fetch }) => {
  const page: WagtailPage = await pageQuery(url, fetch)
  const retPages = await fetch(`/api/blog_pages/`)
  const blogpages: BlogPage[] = await retPages.json()

  const category = url.searchParams.get("category")
  const tag = url.searchParams.get("tag")
  return { page, blogpages, category, tag }
}
