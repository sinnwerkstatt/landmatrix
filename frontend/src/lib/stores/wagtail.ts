import { error, type LoadEvent } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import { writable } from "svelte/store"

import type { ObservatoryPage, WagtailPage } from "$lib/types/wagtail"

export const aboutPages = writable<WagtailPage[]>([])

export async function fetchAboutPages(ftch: LoadEvent["fetch"], locale: string) {
  const indexPageReq = await ftch(
    env.PUBLIC_BASE_URL +
      `/api/wagtail/v2/pages/?order=title&type=wagtailcms.AboutIndexPage`,
  )
  const indexPageReqJson = await indexPageReq.json()
  if (!indexPageReqJson.items || indexPageReqJson.items.length === 0) {
    error(500, "Could not find About IndexPage")
  }
  const indexPageId = indexPageReqJson.items[0].id
  // beware, the $locale doesn't really seem to matter. django is apparently using the cookie anyways.
  const ret = await ftch(
    env.PUBLIC_BASE_URL + `/api/wagtail/v2/pages/?child_of=${indexPageId}`,
    { headers: { "Accept-Language": locale ?? "en" } },
  )
  const retJson = await ret.json()
  aboutPages.set(retJson.items)
}

export const observatoryPages = writable<ObservatoryPage[]>([])

export async function fetchObservatoryPages(fetch: LoadEvent["fetch"], locale: string) {
  type ObservatoryGroups = {
    [key in "global" | "regions" | "countries"]: ObservatoryPage[]
  }
  const ret = await fetch(
    env.PUBLIC_BASE_URL +
      `/api/wagtail/v2/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`,
    { headers: { "Accept-Language": locale ?? "en" } },
  )
  const retJson = await ret.json()
  const pages: ObservatoryPage[] = retJson.items
  const groups: ObservatoryGroups = pages.reduce(
    (acc: ObservatoryGroups, value) => {
      return value.country
        ? { ...acc, countries: [...acc.countries, value] }
        : value.region
          ? { ...acc, regions: [...acc.regions, value] }
          : { ...acc, global: [...acc.global, value] }
    },
    { global: [], regions: [], countries: [] },
  )
  observatoryPages.set([...groups.global, ...groups.regions, ...groups.countries])
}
