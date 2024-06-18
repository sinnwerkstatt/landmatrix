import { error } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient from "openapi-fetch"
import { locale } from "svelte-i18n"
import { derived, readable } from "svelte/store"

import { browser } from "$app/environment"

import { filters, publicOnly } from "$lib/filters"
import type { components, paths } from "$lib/openAPI"
import { loading } from "$lib/stores/basics"
import type { DealHull, InvestorHull } from "$lib/types/data"

export type ValueLabelEntry = components["schemas"]["ValueLabel"]

const serverApiClient = createClient<paths>({ baseUrl: env.PUBLIC_BASE_URL })

export const fieldChoices = derived(
  [locale],
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  ([$locale], set) => {
    serverApiClient.GET("/api/field_choices/").then(ret => {
      // @ts-expect-error openapi-fetch types broken
      if (ret.error) error(500, ret.error)
      set(ret.data)
    })
  },
  {
    deal: {
      intention_of_investment: [],
      intention_of_investment_group: [],
      negotiation_status: [],
      negotiation_status_group: [],
      implementation_status: [],
      level_of_accuracy: [],
      nature_of_deal: [],
      recognition_status: [],
      negative_impacts: [],
      benefits: [],
      former_land_owner: [],
      former_land_use: [],
      ha_area: [],
      community_consultation: [],
      community_reaction: [],
      former_land_cover: [],
      crops: [],
      animals: [],
      electricity_generation: [],
      carbon_sequestration: [],
      carbon_sequestration_certs: [],
      minerals: [],
      water_source: [],
      not_public_reason: [],
      actors: [],
      produce_group: [],
    },
    datasource: { type: [] },
    investor: { classification: [] },
    involvement: { role: [], investment_type: [], parent_relation: [] },
    area: { type: [] },
  } as components["schemas"]["FieldChoices"],
)

// fieldChoices.subscribe(value => console.log(value))

export const createGroupMap = <T extends Record<string, string>>(
  choices: ValueLabelEntry[],
): T =>
  choices.reduce(
    (acc, { value, group }) => ({
      ...acc,
      [value]: group as string,
    }),
    {} as T,
  )

export const createLabels = <T extends string>(
  choices: ValueLabelEntry[],
): { [key in T]: string } =>
  choices.reduce(
    (acc, { value, label }) => ({
      ...acc,
      [value]: label,
    }),
    {} as { [key in T]: string },
  )

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
