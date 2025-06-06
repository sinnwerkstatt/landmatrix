import { redirect } from "@sveltejs/kit"

import type { LayoutLoad } from "./$types"

export const ssr = false

export const load: LayoutLoad = async ({ parent, url }) => {
  const { user } = await parent()

  if (user?.is_authenticated) redirect(301, url.searchParams.get("next") ?? "/")

  return {}
}
