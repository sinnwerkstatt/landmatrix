import type { Client } from "@urql/core";
import { gql } from "@urql/svelte";
import { writable } from "svelte/store";
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

async function getAboutPages(language = "en") {
  console.log("getAboutPages", { language });
  const url = `${RESTEndpoint}/pages/?order=title&type=wagtailcms.AboutIndexPage`;
  const res = await (await fetch(url)).json();
  const indexPageId = res.items[0].id;
  const pagesUrl = `${RESTEndpoint}/pages/?child_of=${indexPageId}`;
  const res_children = await (await fetch(pagesUrl)).json();
  await aboutPages.set(res_children.items);
}

export const observatoryPages = writable<ObservatoryPage[]>([]);

async function getObservatoryPages(language = "en") {
  console.log("getObservatoryPages", { language });
  const url = `${RESTEndpoint}/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`;
  const res = await (await fetch(url)).json();
  await observatoryPages.set(res.items);
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
  await blogCategories.set(data.blogcategories);
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

  await countries.set(data.countries);
  await regions.set(data.regions);
  await formfields.set(data.formfields);
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
  await chartDescriptions.set(data.chart_descriptions);
}

export async function fetchBasis(lang = "en", urqlClient: Client) {
  await getAboutPages(lang);
  await getObservatoryPages(lang);
  await getBlogCategories(lang, urqlClient);
  await getCountriesRegionsFormfields(urqlClient);
  await getChartDescriptions(lang, urqlClient);
}
