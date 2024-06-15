import { error } from "@sveltejs/kit"

import { UserRole } from "$lib/types/data"

import type { PageLoad } from "./$types"

export const ssr = false

export const load: PageLoad = async ({ parent }) => {
  const { user } = await parent()
  if (user.role < UserRole.REPORTER) error(403, "Permission denied")
}
