import { error } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient, { type FetchResponse } from "openapi-fetch"
import type { MediaType } from "openapi-typescript-helpers"

import { i18nload } from "$lib/i18n/i18n"
import type { paths } from "$lib/openAPI"
import { fetchAboutPages, fetchObservatoryPages } from "$lib/stores/wagtail"

import type { LayoutLoad } from "./$types"

export const load: LayoutLoad = async ({ fetch, data }) => {
  const apiClient = createClient<paths>({ baseUrl: env.PUBLIC_BASE_URL, fetch })

  const lang = data.locale ?? "en"

  try {
    const [user, countries, regions] = await Promise.all([
      apiClient
        .GET("/api/users/{id}/", {
          // NOTE: Hack to fetch currently active user
          params: { path: { id: "me" as unknown as number } },
        })
        .then(returnNullOnError),
      apiClient.GET("/api/countries/").then(rejectOnError),
      apiClient.GET("/api/regions/").then(rejectOnError),
      i18nload(lang),
      // TODO: only fetch minimal data needed for layout ,e.g. nav items
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

const returnNullOnError = <T, O, Media extends MediaType>(
  req: FetchResponse<T, O, Media>,
) => (req.error ? null : req.data!)
