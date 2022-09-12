import { error } from "@sveltejs/kit"

import type { PageLoad } from "./$types"

export const ssr = false

export const load: PageLoad = async ({ params, parent }) => {
  const { user } = await parent()
  if (!user) throw error(403, "Permission denied")
}
