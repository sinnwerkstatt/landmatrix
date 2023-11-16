import type { LoadEvent } from "@sveltejs/kit"
import { error } from "@sveltejs/kit"
import type { Client } from "@urql/core"
import { gql } from "@urql/svelte"
import { _ } from "svelte-i18n"
import { derived, get, writable } from "svelte/store"
import type { Writable } from "svelte/store"

import { browser } from "$app/environment"

import {
  flat_intention_of_investment_map,
  intention_of_investment_group_choices,
} from "$lib/choices"
import type { BlockImage } from "$lib/types/custom"
import type { AreaType, IntentionOfInvestment } from "$lib/types/deal"
import {
  ImplementationStatus,
  IntentionOfInvestmentGroup,
  NegotiationStatusGroup,
} from "$lib/types/deal"
import type { DraftStatus, FieldDefinition, Status } from "$lib/types/generics"
import type { User } from "$lib/types/user"
import type {
  BlogCategory,
  Country,
  ObservatoryPage,
  Region,
  WagtailPage,
} from "$lib/types/wagtail"

import type { FormField } from "$components/Fields/fields"

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

export const blogCategories = writable<BlogCategory[]>([])

async function getBlogCategories(language = "en", urqlClient: Client) {
  const { data } = await urqlClient
    .query<{ blogcategories: BlogCategory[] }>(
      gql`
        query ($language: String) {
          blogcategories(language: $language) {
            id
            name
            slug
          }
        }
      `,
      { language },
    )
    .toPromise()
  if (data?.blogcategories) await blogCategories.set(data.blogcategories)
}

type FormFields = {
  deal: { [key: string]: FormField }
  location: { [key: string]: FormField }
  contract: { [key: string]: FormField }
  datasource: { [key: string]: FormField }
  investor: { [key: string]: FormField }
  involvement: { [key: string]: FormField }
}

export const countries = writable<Country[]>([])
export const regions = writable<Region[]>([])
export const formfields = writable<FormFields>(undefined)

async function getCountriesRegionsFormfields(language = "en", urqlClient: Client) {
  const { data } = await urqlClient
    .query(
      gql`
        query ($language: String!) {
          countries {
            id
            name
            code_alpha2
            slug
            point_lat
            point_lon
            point_lat_min
            point_lon_min
            point_lat_max
            point_lon_max
            observatory_page_id
            high_income
            deals {
              id
            }
          }
          regions {
            id
            name
            slug
            point_lat_min
            point_lon_min
            point_lat_max
            point_lon_max
            observatory_page_id
          }
          formfields(language: $language) {
            deal
            location
            contract
            datasource
            investor
            involvement
          }
        }
      `,
      { language },
    )
    .toPromise()

  countries.set(data.countries)
  regions.set(data.regions)
  formfields.set(data.formfields)
}

export const chartDescriptions = writable<{
  web_of_transnational_deals: string
  dynamics_overview: string
  produce_info_map: string
  global_web_of_investments: string
  [key: string]: string
}>(undefined)

async function getChartDescriptions(language = "en", urqlClient: Client) {
  const { data } = await urqlClient
    .query(
      gql`
        query chart_descriptions($language: String) {
          chart_descriptions(language: $language) {
            web_of_transnational_deals
            dynamics_overview
            produce_info_map
            global_web_of_investments
          }
        }
      `,
      { language },
    )
    .toPromise()
  chartDescriptions.set(data.chart_descriptions)
}

export async function fetchBasis(
  lang = "en",
  fetch: LoadEvent["fetch"],
  urqlClient: Client,
) {
  try {
    await Promise.all([
      getAboutPages(fetch),
      getObservatoryPages(fetch),
      getBlogCategories(lang, urqlClient),
      getCountriesRegionsFormfields(lang, urqlClient),
      getChartDescriptions(lang, urqlClient),
    ])
  } catch (e) {
    throw error(500, `Backend server problems ${e}`)
  }
}

export const allUsers = writable<User[]>([])
let fetchingAllUsers = false
export async function getAllUsers(urqlClient: Client) {
  if (get(allUsers).length > 0 || fetchingAllUsers) return
  fetchingAllUsers = true
  const ret = await urqlClient
    .query<{ users: User[] }>(
      gql`
        {
          users {
            id
            full_name
            username
            role
          }
        }
      `,
      {},
    )
    .toPromise()
  if (!ret.data?.users) throw error(500, "could not fetch users from database")

  const usrs = ret.data.users.sort((a, b) => a.full_name.localeCompare(b.full_name))
  allUsers.set(usrs)
  fetchingAllUsers = false
}

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

export const isMobile: Writable<boolean | null> = writable(null)

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

export const fieldDefinitions: Writable<FieldDefinition[]> = writable([])
export async function fetchFieldDefinitions(fetch: LoadEvent["fetch"]) {
  const res = await fetch("/api/field_definitions/")
  fieldDefinitions.set(await res.json())
}

export const contentRootElement: Writable<HTMLElement> = writable()
