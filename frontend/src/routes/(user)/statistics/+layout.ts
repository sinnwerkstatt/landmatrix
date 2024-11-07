import { error } from "@sveltejs/kit"

import { isReporterOrAbove } from "$lib/utils/permissions"

import type { LayoutLoad } from "./$types"

export const ssr = false

export const load: LayoutLoad = async ({ url, parent }) => {
  const { user } = await parent()

  if (!isReporterOrAbove(user)) error(403, "Permission denied")

  return { url }
}
