import { redirect } from "@sveltejs/kit"

import type { PageLoad } from "./$types"

export const load: PageLoad = async () => {
  redirect(301, "/docs/api/?from_graphql=true")
}
