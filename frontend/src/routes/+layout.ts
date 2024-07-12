import { error, type LoadEvent } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient, { type FetchResponse } from "openapi-fetch"
import type { MediaType } from "openapi-typescript-helpers"

import { i18nload } from "$lib/i18n/i18n"
import type { paths } from "$lib/openAPI"
import { fetchAboutPages, fetchObservatoryPages } from "$lib/stores/wagtail"
import type { User } from "$lib/types/data"

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

  // TODO: only fetch minimal data needed for layout ,e.g. nav items
  try {
    const [countries, regions] = await Promise.all([
      apiClient.GET("/api/countries/").then(rejectOnError),
      apiClient.GET("/api/regions/").then(rejectOnError),
      // needed by nav
      fetchObservatoryPages(fetch, lang),
      fetchAboutPages(fetch, lang),
    ])
    return { apiClient, user, countries, regions }
  } catch (e) {
    throw error(500, "Layout Load Error")
  }
}

const rejectOnError = <T, O, Media extends MediaType>(
  req: FetchResponse<T, O, Media>,
) => (req.error ? Promise.reject(req.error.detail) : req.data!)
