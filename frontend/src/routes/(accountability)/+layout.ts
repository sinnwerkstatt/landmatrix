import { error } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient from "openapi-fetch"

import type { components, paths } from "$lib/openAPI"

export async function load() {
  // Fetching extra elements from api, see +layout.ts at the root of the site
  const apiClient = createClient<paths>({ baseUrl: env.PUBLIC_BASE_URL, fetch })

  const investorsReq = await apiClient.GET("/api/investors/simple/")
  if (investorsReq.error) error(500, investorsReq.error)
  const investors: components["schemas"]["SimpleInvestor"][] = investorsReq.data

  const vggtVariablesReq = await apiClient.GET("/api/accountability/variable/")
  if (vggtVariablesReq.error) error(500, vggtVariablesReq.error)
  const vggtVariables: components["schemas"]["VggtVariable"][] = vggtVariablesReq.data

  const vggtArticlesReq = await apiClient.GET("/api/accountability/article/")
  if (vggtArticlesReq.error) error(500, vggtArticlesReq.error)
  const vggtArticles: components["schemas"]["VggtArticle"][] = vggtArticlesReq.data

  return { investors, vggtVariables, vggtArticles }
}
