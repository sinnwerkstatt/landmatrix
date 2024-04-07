import { error } from "@sveltejs/kit"
import { env } from "$env/dynamic/public"
import createClient from "openapi-fetch"
import { _, locale } from "svelte-i18n"
import { derived, readable, writable } from "svelte/store"

import { browser } from "$app/environment"

import {
  flat_intention_of_investment_map,
  intention_of_investment_group_choices,
} from "$lib/choices"
import { filters, publicOnly } from "$lib/filters"
import type { components, paths } from "$lib/openAPI"
import { loading } from "$lib/stores/basics"
import type { AreaType, IntentionOfInvestment } from "$lib/types/deal"
import {
  ImplementationStatus,
  IntentionOfInvestmentGroup,
  NegotiationStatusGroup,
} from "$lib/types/deal"
import type { Currency, DealHull, InvestorHull } from "$lib/types/newtypes"
import type { Country, Region } from "$lib/types/wagtail"

export interface ValueLabelEntry {
  value: string
  label: string
  group?: string
}

const serverApiClient = createClient<paths>({ baseUrl: env.PUBLIC_BASE_URL })

export const fieldChoices = readable<components["schemas"]["FieldChoices"]>(
  {
    deal: {
      intention_of_investment: [],
      negotiation_status: [],
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
    },
    datasource: {
      type: [],
    },
    investor: { classification: [] },
    involvement: { role: [], investment_type: [], parent_relation: [] },
  },
  set => {
    serverApiClient.GET("/api/field_choices/").then(ret => {
      if (ret.error) error(500, ret.error)
      set(ret.data)
    })
  },
)

export const blogCategories = readable(
  [] as components["schemas"]["BlogCategory"][],
  set => {
    serverApiClient.GET("/api/blog_categories/").then(ret => {
      if (ret.error) error(500, ret.error)
      set(ret.data)
    })
  },
)

export const chartDescriptions = derived(
  [locale],
  ([$locale], set) => {
    serverApiClient
      .GET(`/api/chart_descriptions/`, { params: { query: { lang: $locale } } })
      .then(ret => {
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
    if (ret.error) error(500, ret.error)
    set(ret.data)
  })
})

type ImplementationStatusMap = { [key in ImplementationStatus]: string }
export const implementationStatusMap = derived(
  _,
  ($_): ImplementationStatusMap => ({
    [ImplementationStatus.PROJECT_NOT_STARTED]: $_("Project not started"),
    [ImplementationStatus.STARTUP_PHASE]: $_("Startup phase (no production)"),
    [ImplementationStatus.IN_OPERATION]: $_("In operation (production)"),
    [ImplementationStatus.PROJECT_ABANDONED]: $_("Project abandoned"),
  }),
)

type NegotiationStatusGroupMap = { [key in NegotiationStatusGroup]: string }
export const negotiationStatusGroupMap = derived(
  _,
  ($_): NegotiationStatusGroupMap => ({
    [NegotiationStatusGroup.INTENDED]: $_("Intended"),
    [NegotiationStatusGroup.CONCLUDED]: $_("Concluded"),
    [NegotiationStatusGroup.FAILED]: $_("Failed"),
    [NegotiationStatusGroup.CONTRACT_EXPIRED]: $_("Contract expired"),
  }),
)

type IntentionOfInvestmentGroupMap = { [key in IntentionOfInvestmentGroup]: string }
export const intentionOfInvestmentGroupMap = derived(
  _,
  ($_): IntentionOfInvestmentGroupMap =>
    Object.fromEntries(
      Object.entries(intention_of_investment_group_choices).map(([key, value]) => [
        key,
        $_(value),
      ]),
    ) as IntentionOfInvestmentGroupMap,
)

type IntentionOfInvestmentMap = { [key in IntentionOfInvestment]: string }
export const intentionOfInvestmentMap = derived(
  _,
  ($_): IntentionOfInvestmentMap =>
    Object.fromEntries(
      Object.entries(flat_intention_of_investment_map).map(([key, value]) => [
        key,
        $_(value),
      ]),
    ) as IntentionOfInvestmentMap,
)

type AreaTypeMap = { [key in AreaType]: string }
export const areaTypeMap = derived(
  _,
  ($_): AreaTypeMap => ({
    production_area: $_("Production area"),
    contract_area: $_("Contract area"),
    intended_area: $_("Intended area"),
  }),
)

interface FieldDefinition {
  id: number
  model: "deal" | "investor"
  field: string
  short_description: string
  long_description: string
  editor_description: string
}

export const fieldDefinitions = derived(
  [locale],
  ([$locale], set) => {
    fetch(env.PUBLIC_BASE_URL + "/api/field_definitions/", {
      headers: { "Accept-Language": $locale ?? "en" },
    })
      .then(ret => ret.json() as Promise<FieldDefinition[]>)
      .then(set)
  },
  [] as FieldDefinition[],
)

export const currencies = readable<Currency[]>([], set => {
  fetch("/api/currencies/")
    .then(ret => ret.json())
    .then(set)
})
export const countries = readable<Country[]>([], set => {
  if (browser)
    fetch(env.PUBLIC_BASE_URL + "/api/countries/")
      .then(ret => ret.json())
      .then(set)
})
export const regions = readable<Region[]>([], set => {
  fetch(env.PUBLIC_BASE_URL + "/api/regions/")
    .then(ret => ret.json())
    .then(set)
})

export const contentRootElement = writable<HTMLElement>()

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

export interface SimpleInvestor {
  id: number
  name: string
}

export const simpleInvestors = readable(
  [] as components["schemas"]["SimpleInvestor"][],
  set => {
    serverApiClient.GET("/api/investors/simple/").then(ret => {
      if (ret.error) error(500, ret.error)
      set(ret.data)
    })
  },
)
