import { error } from "@sveltejs/kit"
import { get, writable } from "svelte/store"

import type { components } from "$lib/openAPI"
import { pageQuery } from "$lib/queries"
import type { WagtailPage } from "$lib/types/wagtail"

import type { PageLoad } from "./$types"

const blogpages = writable<components["schemas"]["BlogPage"][]>([])

export const load: PageLoad = async ({ url, fetch, parent }) => {
  const { apiClient } = await parent()
  const page: WagtailPage = await pageQuery(url, fetch)

  if (get(blogpages).length === 0) {
    const retPages = await apiClient.GET(`/api/blog_pages/`)
    if (retPages.error) error(500, retPages.error)
    blogpages.set(retPages.data)
  }

  const category = url.searchParams.get("category")
  const tag = url.searchParams.get("tag")
  return { page, blogpages, category, tag }
}
