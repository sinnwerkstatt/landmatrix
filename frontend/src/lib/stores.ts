import type { LoadEvent } from "@sveltejs/kit"
import { error } from "@sveltejs/kit"
import type { GeoJSON } from "leaflet"
import { _, locale } from "svelte-i18n"
import { derived, readable, writable } from "svelte/store"

import { browser } from "$app/environment"

import {
  flat_intention_of_investment_map,
  intention_of_investment_group_choices,
} from "$lib/choices"
import { filters, publicOnly } from "$lib/filters"
import type { BlockImage } from "$lib/types/custom"
import type { AreaType, IntentionOfInvestment } from "$lib/types/deal"
import {
  ImplementationStatus,
  IntentionOfInvestmentGroup,
  NegotiationStatusGroup,
} from "$lib/types/deal"
import type { DraftStatus, FieldDefinition, Status } from "$lib/types/generics"
import type { Currency, DealHull, InvestorHull } from "$lib/types/newtypes"
import type { User } from "$lib/types/user"
import type {
  BlogCategory,
  Country,
  ObservatoryPage,
  Region,
  WagtailPage,
} from "$lib/types/wagtail"

export const aboutPages = writable<WagtailPage[]>([])

async function getAboutPages(fetch: LoadEvent["fetch"]) {
  const url = `/api/wagtail/v2/pages/?order=title&type=wagtailcms.AboutIndexPage`
  const res = await (
    await fetch(url, { headers: { Accept: "application/json" } })
  ).json()
  if (res.items && res.items.length) {
    const indexPageId = res.items[0].id
    const pagesUrl = `/api/wagtail/v2/pages/?child_of=${indexPageId}`
    const res_children = await (
      await fetch(pagesUrl, { headers: { Accept: "application/json" } })
    ).json()
    aboutPages.set(res_children.items)
  }
}

export interface ValueLabelEntry {
  value: string
  label: string
  group?: string
}

interface FieldChoicesType {
  deal: {
    intention_of_investment: ValueLabelEntry[]
    negotiation_status: ValueLabelEntry[]
    implementation_status: ValueLabelEntry[]
    level_of_accuracy: ValueLabelEntry[]
    nature_of_deal: ValueLabelEntry[]
    recognition_status: ValueLabelEntry[]
    negative_impacts: ValueLabelEntry[]
    benefits: ValueLabelEntry[]
    former_land_owner: ValueLabelEntry[]
    former_land_use: ValueLabelEntry[]
    ha_area: ValueLabelEntry[]
    community_consultation: ValueLabelEntry[]
    community_reaction: ValueLabelEntry[]
    former_land_cover: ValueLabelEntry[]
    crops: ValueLabelEntry[]
    animals: ValueLabelEntry[]
    electricity_generation: ValueLabelEntry[]
    carbon_sequestration: ValueLabelEntry[]
    carbon_sequestration_certs: ValueLabelEntry[]
    minerals: ValueLabelEntry[]
    water_source: ValueLabelEntry[]
    not_public_reason: ValueLabelEntry[]
    actors: ValueLabelEntry[]
  }
  datasource: {
    type: ValueLabelEntry[]
  }
  investor: {
    classification: ValueLabelEntry[]
  }
  involvement: {
    investment_type: ValueLabelEntry[]
  }
}

export const fieldChoices = readable<FieldChoicesType>(
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
    involvement: { investment_type: [] },
  },
  set => {
    fetch(`/api/field_choices/`, { headers: { Accept: "application/json" } })
      .then(ret => ret.json())
      .then(set)
  },
)

export const observatoryPages = writable<ObservatoryPage[]>([])

type ObservatoryGroups = {
  [key in "global" | "regions" | "countries"]: ObservatoryPage[]
}

async function getObservatoryPages(fetch: LoadEvent["fetch"]) {
  const url = `/api/wagtail/v2/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`
  const res = await (
    await fetch(url, { headers: { Accept: "application/json" } })
  ).json()
  const pages: ObservatoryPage[] = res.items
  const groups: ObservatoryGroups = pages.reduce(
    (acc: ObservatoryGroups, value) => {
      if (value.country) {
        return { ...acc, countries: [...acc.countries, value] }
      }
      if (value.region) {
        return { ...acc, regions: [...acc.regions, value] }
      }
      return { ...acc, global: [...acc.global, value] }
    },
    { global: [], regions: [], countries: [] },
  )
  observatoryPages.set([...groups.global, ...groups.regions, ...groups.countries])
}

export const blogCategories = readable([] as BlogCategory[], set => {
  if (browser) {
    fetch(`/api/blog_categories/`)
      .then(ret => ret.json() as Promise<BlogCategory[]>)
      .then(set)
  }
})

interface ChartDesc {
  web_of_transnational_deals: string
  dynamics_overview: string
  produce_info_map: string
  global_web_of_investments: string

  [key: string]: string
}

export const chartDescriptions = derived(
  [locale],
  ([$locale], set) => {
    fetch(`/api/chart_descriptions/?lang=${$locale}`)
      .then(ret => ret.json() as Promise<ChartDesc>)
      .then(set)
  },
  {} as ChartDesc,
)

export async function fetchBasis(fetch: LoadEvent["fetch"]) {
  try {
    await Promise.all([getAboutPages(fetch), getObservatoryPages(fetch)])
  } catch (e) {
    error(500, `Backend server problems ${e}`)
  }
}

// export const allUsers = writable<User[]>([])
// let fetchingAllUsers = false
// export async function getAllUsers(fetch: LoadEvent["fetch"]) {
//   if (get(allUsers).length > 0 || fetchingAllUsers) return
//   fetchingAllUsers = true
//   const ret = await fetch("/api/users/")
//   const users = await ret.json()
//   if (!users) throw error(500, "could not fetch users from database")
//
//   allUsers.set(users)
//   fetchingAllUsers = false
// }

export const allUsers = readable([] as User[], set => {
  if (!browser) {
    set([])
    return
  }
  fetch(`/api/users/`)
    .then(ret => {
      if (!ret.ok) throw new Error(`HTTP status code: ${ret.status}\n\n${ret}`)
      return ret.json() as Promise<User[]>
    })
    .then(set)
    .catch(() => set([]))
})

export const loading = writable(false)

type StatusMap = { [key in Status]: string }
export const statusMap = derived(
  _,
  ($_): StatusMap => ({
    1: $_("Draft"),
    2: $_("Active"), //"Live",
    3: $_("Active"), // "Updated",
    4: $_("Deleted"),
    5: $_("Rejected"), // legacy
    6: $_("To Delete"), // legacy
  }),
)

type DraftStatusMap = { [key in DraftStatus]: string }
export const draftStatusMap = derived(
  _,
  ($_): DraftStatusMap => ({
    1: $_("Draft"),
    2: $_("Review"),
    3: $_("Activation"),
    4: $_("Rejected"), // legacy
    5: $_("Deleted"),
  }),
)

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

export const lightboxImage = writable<BlockImage | null>(null)

export const isDarkMode = writable(false)

const bindIsDarkModeToPreferredColorScheme = () => {
  if (window.matchMedia) {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)")

    isDarkMode.set(mediaQuery.matches)
    mediaQuery.addEventListener("change", event => {
      isDarkMode.set(event.matches)
    })
  }
}

export const isMobile = writable<boolean | null>(null)

const TAILWIND_SM_BREAKPOINT_IN_PX = 640

const bindIsMobileToScreenInnerWidth = () => {
  isMobile.set(window.innerWidth <= TAILWIND_SM_BREAKPOINT_IN_PX)

  window.addEventListener("resize", () => {
    isMobile.set(window.innerWidth <= TAILWIND_SM_BREAKPOINT_IN_PX)
  })
}

if (browser) {
  bindIsDarkModeToPreferredColorScheme()
  bindIsMobileToScreenInnerWidth()
}

// export const fieldDefinitions = readable<FieldDefinition[]>([], set=>{
//   fetch("/api/field_definitions/").then(ret=>ret.json()).then(set)
// })
export const fieldDefinitions = writable<FieldDefinition[]>([])

export async function fetchFieldDefinitions(fetch: LoadEvent["fetch"]) {
  const res = await fetch("/api/field_definitions/")
  fieldDefinitions.set(await res.json())
}

export const currencies = readable<Currency[]>([], set => {
  fetch("/api/currencies/")
    .then(ret => ret.json())
    .then(set)
})
export const countries = readable<Country[]>([], set => {
  fetch("/api/countries/")
    .then(ret => ret.json())
    .then(set)
})
export const regions = readable<Region[]>([], set => {
  fetch("/api/regions/")
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

export const simpleInvestors = readable<SimpleInvestor[]>([], set => {
  fetch("/api/investors/simple")
    .then(ret => ret.json())
    .then(set)
})

export const geoJsonLayerGroup = writable<GeoJSON | null>(null)
