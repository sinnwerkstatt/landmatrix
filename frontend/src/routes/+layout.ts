import type { LoadEvent } from "@sveltejs/kit"
import { cacheExchange, Client, fetchExchange } from "@urql/core"

import { i18nload } from "$lib/i18n/i18n"
import { fetchBasis } from "$lib/stores"
import type { User } from "$lib/types/user"

import type { LayoutLoad } from "./$types"

// ssr turned on by default
// https://kit.svelte.dev/docs/page-options#ssr

async function fetchMe(fetch: LoadEvent["fetch"]) {
  const ret = await fetch("/api/users/me/", {
    credentials: "include",
  })
  if (ret.ok) return (await ret.json()) as User

  return null
}

export const load: LayoutLoad = async ({ fetch, data }) => {
  const urqlClient = new Client({
    url: "/graphql/",
    exchanges: [cacheExchange, fetchExchange],
    fetch,
    fetchOptions: () => ({ credentials: "include" }),
  })

  // fetch("adsf", {})
  const user: User | null = await fetchMe(fetch)
  const lang = data?.locale ?? "en"
  await Promise.all([fetchBasis(lang, fetch), i18nload(lang)])

  return { urqlClient, user }
}
