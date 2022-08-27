import type { LoadEvent } from "@sveltejs/kit";
import { error } from "@sveltejs/kit";
import type { Client } from "@urql/core";
import { gql } from "@urql/svelte";
import { get, writable } from "svelte/store";
import type { Writable } from "svelte/store";
import type { User } from "$lib/types/user";
import type {
  BlogCategory,
  Country,
  ObservatoryPage,
  Region,
  WagtailPage,
} from "$lib/types/wagtail";
import type { FormField } from "$components/Fields/fields";

const RESTEndpoint = `${import.meta.env.VITE_BASE_URL}/wagtailapi/v2`;

export const aboutPages = writable<WagtailPage[]>([]);

async function getAboutPages(language = "en", fetch: LoadEvent["fetch"]) {
  console.log("getAboutPages", { language });
  const url = `${RESTEndpoint}/pages/?order=title&type=wagtailcms.AboutIndexPage`;
  const res = await (
    await fetch(url, { headers: { Accept: "application/json" } })
  ).json();
  const indexPageId = res.items[0].id;
  const pagesUrl = `${RESTEndpoint}/pages/?child_of=${indexPageId}`;
  const res_children = await (
    await fetch(pagesUrl, { headers: { Accept: "application/json" } })
  ).json();
  aboutPages.set(res_children.items);
}

export const observatoryPages = writable<ObservatoryPage[]>([]);

async function getObservatoryPages(language = "en", fetch: LoadEvent["fetch"]) {
  console.log("getObservatoryPages", { language });
  const url = `${RESTEndpoint}/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`;
  const res = await (
    await fetch(url, { headers: { Accept: "application/json" } })
  ).json();
  observatoryPages.set(res.items);
}

export const blogCategories = writable<BlogCategory[]>([]);

async function getBlogCategories(language = "en", urqlClient: Client) {
  console.log("getBlogCategories", { language });
  const { data } = await urqlClient
    .query(
      gql`
        query ($language: String) {
          blogcategories(language: $language) {
            id
            name
            slug
          }
        }
      `,
      { language }
    )
    .toPromise();
  blogCategories.set(data.blogcategories);
}

type FormFields = {
  deal: { [key: string]: FormField };
  location: { [key: string]: FormField };
  contract: { [key: string]: FormField };
  datasource: { [key: string]: FormField };
  investor: { [key: string]: FormField };
  involvement: { [key: string]: FormField };
};

export const countries = writable<Country[]>([]);
export const regions = writable<Region[]>([]);
export const formfields = writable<FormFields>(undefined);

async function getCountriesRegionsFormfields(urqlClient: Client) {
  console.log("getCountriesRegionsFormfields");
  const { data } = await urqlClient
    .query(
      gql`
        query {
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
          formfields {
            deal
            location
            contract
            datasource
            investor
            involvement
          }
        }
      `,
      {}
    )
    .toPromise();

  countries.set(data.countries);
  regions.set(data.regions);
  formfields.set(data.formfields);
}

export const chartDescriptions = writable<{
  web_of_transnational_deals: string;
  dynamics_overview: string;
  produce_info_map: string;
}>(undefined);

async function getChartDescriptions(language = "en", urqlClient: Client) {
  console.log("getChartDescriptions", { language });
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
      { language }
    )
    .toPromise();
  chartDescriptions.set(data.chart_descriptions);
}

export async function fetchBasis(
  lang = "en",
  fetch: LoadEvent["fetch"],
  urqlClient: Client
) {
  try {
    await Promise.all([
      getAboutPages(lang, fetch),
      getObservatoryPages(lang, fetch),
      getBlogCategories(lang, urqlClient),
      getCountriesRegionsFormfields(urqlClient),
      getChartDescriptions(lang, urqlClient),
    ]);
  } catch (e) {
    throw error(500, "Backend server problems");
  }
}

/// client stores - MAKE SURE THESE DON'T GET CALLED FROM SSR-FUNCTIONS!
export const users = writable<User[]>([]);

export async function getUsers(urqlClient: Client): Promise<Writable<User[]>> {
  if (get(users).length > 0) return users;
  const ret = await urqlClient
    .query<{ users: User[] }>(
      gql`
        {
          users {
            id
            full_name
            username
          }
        }
      `,
      {}
    )
    .toPromise();
  if (!ret.data?.users) throw error(500, "could not fetch users");
  await users.set(
    ret.data.users.sort((a, b) => a.full_name.localeCompare(b.full_name))
  );
  return users;
}

export const loading = writable(false);
