import { error } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient from "openapi-fetch"

import type { components, paths } from "$lib/openAPI"

export async function load() {
  // Fetching extra elements from api, see +layout.ts at the root of the site
  const apiClient = createClient<paths>({ baseUrl: env.PUBLIC_BASE_URL, fetch })

  const fieldChoicesReq = await apiClient.GET("/api/field_choices/")
  if (fieldChoicesReq.error) error(500, fieldChoicesReq.error)
  const fieldChoices: components["schemas"]["FieldChoices"][] = fieldChoicesReq.data

  const investorsReq = await apiClient.GET("/api/investors/simple/")
  if (investorsReq.error) error(500, investorsReq.error)
  const investors: components["schemas"]["SimpleInvestor"][] = investorsReq.data

  const vggtVariablesReq = await apiClient.GET("/api/accountability/variable/")
  if (vggtVariablesReq.error) error(500, vggtVariablesReq.error)
  const vggtVariables: components["schemas"]["VggtVariable"][] = vggtVariablesReq.data

  return { fieldChoices, investors, vggtVariables }
}
