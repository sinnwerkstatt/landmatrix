import { redirect } from "@sveltejs/kit"

import type { PageServerLoad } from "../../../../.svelte-kit/types/src/routes"

export const load: PageServerLoad = async ({ url }) => {
  redirect(307, new URL("quality/deal/", url))
}
