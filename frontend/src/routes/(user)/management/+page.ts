import { error } from "@sveltejs/kit"

import type { PageLoad } from "../../../../../.svelte-kit/types/src/routes"

export const ssr = false

export const load: PageLoad = async ({ parent }) => {
  const { user } = await parent()
  if (!user) error(403, "Permission denied")
}
