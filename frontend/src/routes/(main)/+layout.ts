import type { components } from "$lib/openAPI"

import type { LayoutLoad } from "./$types"

export const ssr = false

export const load: LayoutLoad = async ({ parent }) => {
  const { apiClient } = await parent()

  let contextHelp: components["schemas"]["ContextHelp"][] | undefined
  const chRes = await apiClient.GET("/api/context_help/")
  if ("error" in chRes) {
    // error(chRes.response.status, JSON.stringify(chRes.error))
  } else {
    contextHelp = chRes.data
  }

  return { contextHelp }
}
