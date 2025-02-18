import { error } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient from "openapi-fetch"
import { locale } from "svelte-i18n"
import { derived, readable, writable } from "svelte/store"

import { browser } from "$app/environment"

import { filters, publicOnly } from "$lib/filters"
import type { components, paths } from "$lib/openAPI"
import { loading } from "$lib/stores/basics"
import type { DealHull, InvestorHull } from "$lib/types/data"

const serverApiClient = createClient<paths>({ baseUrl: env.PUBLIC_BASE_URL })

// export const findChoice = (
//   choices: ValueLabelEntry[],
//   value: string,
// ): ValueLabelEntry | undefined => choices.find(x => x.value === value)
//
// export const getFieldChoicesLabel =
//   (choices: ValueLabelEntry[]) =>
//   (value: string): string | undefined =>
//     findChoice(choices, value)?.label
//
// export const getFieldChoicesGroup =
//   (choices: ValueLabelEntry[]) =>
//   (value: string): string | undefined =>
//     findChoice(choices, value)?.group

export const blogCategories = derived(
  [locale],
  ([$locale], set) => {
    serverApiClient
      .GET("/api/blog_categories/", { params: { query: { lang: $locale } } })
      .then(ret => {
        // @ts-expect-error openapi-fetch types broken
        if (ret.error) error(500, ret.error)
        set(ret.data)
      })
  },
  [] as components["schemas"]["BlogCategory"][],
)

export const chartDescriptions = derived(
  [locale],
  ([$locale], set) => {
    serverApiClient
      .GET(`/api/chart_descriptions/`, { params: { query: { lang: $locale } } })
      .then(ret => {
        // @ts-expect-error openapi-fetch types broken
        if (ret.error) error(500, ret.error)
        set(ret.data)
      })
  },
  {
    web_of_transnational_deals: "",
    dynamics_overview: "",
    produce_info_map: "",
    global_web_of_investments: "",
  } as components["schemas"]["ChartDescriptions"],
)

export const allUsers = readable([] as components["schemas"]["LeanUser"][], set => {
  if (!browser) {
    set([])
    return
  }
  serverApiClient.GET("/api/users/").then(ret => {
    // @ts-expect-error openapi-fetch types broken
    if (ret.error) error(500, ret.error)
    set(ret.data)
  })
})

export const currencies = readable<components["schemas"]["Currency"][]>([], set => {
  serverApiClient.GET("/api/currencies/").then(ret => {
    // @ts-expect-error openapi-fetch types broken
    if (ret.error) error(500, ret.error)
    set(ret.data)
  })
})

export const dealsNG = derived(
  [filters, publicOnly],
  ([$filters, $publicOnly], set) => {
    loading.set(true)
    const subset = $publicOnly ? "PUBLIC" : "ACTIVE"
    fetch(`/api/deals/?subset=${subset}&${$filters.toRESTFilterArray()}`)
      .then(ret => ret.json() as Promise<DealHull[]>)
      .then(ret => {
        loading.set(false)
        set(ret)
      })
  },
  [] as DealHull[],
)

export const investorsNG = derived(
  [filters, publicOnly],
  ([$filters, $publicOnly], set) => {
    loading.set(true)
    const subset = $publicOnly ? "PUBLIC" : "ACTIVE"
    fetch(
      `/api/investors/deal_filtered/?subset=${subset}&${$filters.toRESTFilterArray()}`,
    )
      .then(ret => ret.json() as Promise<InvestorHull[]>)
      .then(ret => {
        loading.set(false)
        set(ret)
      })
  },
  [] as InvestorHull[],
)

export const simpleInvestors = readable(
  [] as components["schemas"]["SimpleInvestor"][],
  set => {
    serverApiClient.GET("/api/investors/simple/").then(ret => {
      // @ts-expect-error openapi-fetch types broken
      if (ret.error) error(500, ret.error)
      set(ret.data)
    })
  },
)

function createContextHelpStore() {
  let showContextHelp = true
  if (browser) showContextHelp = localStorage.showContextHelp !== "false"

  const { subscribe, set, update } = writable(showContextHelp)

  return {
    subscribe,
    set,
    toggle: () =>
      update(n => {
        if (browser) localStorage.showContextHelp = n ? "false" : "true"
        return !n
      }),
  }
}

export const showContextHelp = createContextHelpStore()
