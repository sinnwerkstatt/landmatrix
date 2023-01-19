import type { LoadEvent } from "@sveltejs/kit"
import { error } from "@sveltejs/kit"
import type { Client } from "@urql/core"
import { gql } from "@urql/svelte"
import { _ } from "svelte-i18n"
import { derived, get, writable } from "svelte/store"

import type { DraftStatus, Status } from "$lib/types/generics"
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
  // console.log("getAboutPages")
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

async function getObservatoryPages(fetch: LoadEvent["fetch"]) {
  // console.log("getObservatoryPages", { language })
  const url = `/api/wagtail/v2/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`
  const res = await (
    await fetch(url, { headers: { Accept: "application/json" } })
  ).json()
  observatoryPages.set(res.items)
}

export const blogCategories = writable<BlogCategory[]>([])

async function getBlogCategories(language = "en", urqlClient: Client) {
  // console.log("getBlogCategories", { language })
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
  // console.log("getCountriesRegionsFormfields")
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
}>(undefined)

async function getChartDescriptions(language = "en", urqlClient: Client) {
  // console.log("getChartDescriptions", { language })
  const { data } = await urqlClient
    .query(
      gql`
        query chart_descriptions($language: String) {
          chart_descriptions(language: $language) {
            web_of_transnational_deals
            dynamics_overview
            produce_info_map
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
