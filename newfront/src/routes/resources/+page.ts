import { gql } from "@urql/svelte"

import { pageQuery } from "$lib/queries"
import type { BlogPage, WagtailPage } from "$lib/types/wagtail"

import type { PageLoad } from "./$types"

export const load: PageLoad = async ({ url, fetch, parent }) => {
  const { urqlClient } = await parent()
  const page: WagtailPage = await pageQuery(url, fetch)
  const returql = await urqlClient
    .query<{ blogpages: BlogPage[] }>(
      gql`
        query {
          blogpages {
            id
            title
            slug
            date
            header_image
            excerpt
            categories {
              slug
            }
            tags {
              slug
            }
            url
          }
        }
      `,
      {},
    )
    .toPromise()
  const category = url.searchParams.get("category")
  const tag = url.searchParams.get("tag")
  return { page, blogpages: returql?.data?.blogpages, category, tag }
}
