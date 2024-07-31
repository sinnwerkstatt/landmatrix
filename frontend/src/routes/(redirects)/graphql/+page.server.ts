import { redirect } from "@sveltejs/kit"

import type { PageServerLoad } from "./$types"

export const load: PageServerLoad = async () => {
  redirect(301, "/docs/api/?from_graphql=true")
}
