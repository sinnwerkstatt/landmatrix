import { redirect } from "@sveltejs/kit"

import type { PageServerLoad } from "./$types"

export const load: PageServerLoad = () => {
  throw redirect(307, "/about/the-land-matrix-initiative/")
}
