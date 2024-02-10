import type { LoadEvent } from "@sveltejs/kit"

import { i18nload } from "$lib/i18n/i18n"
import type { User } from "$lib/types/user"

import type { LayoutLoad } from "./$types"

// ssr turned on by default
// https://kit.svelte.dev/docs/page-options#ssr

async function fetchMe(fetch: LoadEvent["fetch"]) {
  const ret = await fetch("/api/users/me/", { credentials: "include" })
  if (ret.ok) return (await ret.json()) as User
  return null
}

export const load: LayoutLoad = async ({ fetch, data }) => {
  const user: User | null = await fetchMe(fetch)
  const lang = data?.locale ?? "en"
  await i18nload(lang)

  return { user }
}
