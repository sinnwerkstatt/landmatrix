import { error } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient from "openapi-fetch"

// import { _ } from "svelte-i18n"

import type { components, paths } from "$lib/openAPI"

export async function load({ params, fetch }) {
  const apiClient = createClient<paths>({ baseUrl: env.PUBLIC_BASE_URL, fetch })
  let project = {}

  if (params.project != "0") {
    const projectReq = await apiClient.GET(
      `/api/accountability/project/${params.project}/`,
    )
    if (projectReq.error) error(500, projectReq.error.detail)
    const res: components["schemas"]["Project"][] = projectReq.data
    project = res
  }

  return { project }
}
