import { error } from "@sveltejs/kit"

import { isReporterOrAbove } from "$lib/utils/permissions"

import type { PageLoad } from "./$types"

export const ssr = false

export const load: PageLoad = async ({ parent }) => {
  const { user } = await parent()
  if (!isReporterOrAbove(user)) error(403, "Permission denied")
}
