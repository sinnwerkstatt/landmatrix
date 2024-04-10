import { error, type LoadEvent } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient from "openapi-fetch"

import { i18nload } from "$lib/i18n/i18n"
import type { components, paths } from "$lib/openAPI"
import { fetchAboutPages, fetchObservatoryPages } from "$lib/stores/wagtail"
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
  const apiClient = createClient<paths>({ baseUrl: env.PUBLIC_BASE_URL, fetch })

  const user: User | null = await fetchMe(fetch)
  const lang = data?.locale ?? "en"
  await i18nload(lang)

  await fetchObservatoryPages(fetch, lang)
  await fetchAboutPages(fetch, lang)

  const countriesReq = await apiClient.GET("/api/countries/")
  if (countriesReq.error) error(500, countriesReq.error)
  const countries: components["schemas"]["Country"][] = countriesReq.data

  const regionsReq = await apiClient.GET("/api/regions/")
  if (regionsReq.error) error(500, regionsReq.error)
  const regions: components["schemas"]["Region"][] = regionsReq.data

  return { apiClient, user, countries, regions }
}
