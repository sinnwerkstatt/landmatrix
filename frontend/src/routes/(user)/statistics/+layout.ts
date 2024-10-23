import { error } from "@sveltejs/kit"

import { isEditorOrAbove } from "$lib/utils/permissions"

import type { LayoutLoad } from "../../../../.svelte-kit/types/src/routes"

export const ssr = false

export const load: LayoutLoad = async ({ url, parent }) => {
  const { user } = await parent()

  if (!isEditorOrAbove(user)) error(403, "Permission denied")
  return { url }
}
