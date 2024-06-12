import { redirect } from "@sveltejs/kit"

import type { PageLoad } from "./$types"

export const load: PageLoad = ({ url }) => {
  redirect(307, new URL("locations", url))
}
