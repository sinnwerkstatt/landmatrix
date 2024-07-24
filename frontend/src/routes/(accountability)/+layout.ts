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

  return { fieldChoices }
}
