import { gql } from "@apollo/client/core";
import { get, writable } from "svelte/store";
import type { User } from "$lib/types/user";
import type {
  BlogCategory,
  Country,
  ObservatoryPage,
  Region,
  WagtailPage,
} from "$lib/types/wagtail";
import type { FormField } from "$components/Fields/fields";
import { client } from "./apolloClient";
import { RESTEndpoint } from "./index";

export const observatoryPages = writable<ObservatoryPage[]>([]);

async function getObservatoryPages(language = "en") {
  console.log("getObservatoryPages", { language });
  const observatoriesStore = get(observatoryPages);
  if (observatoriesStore !== undefined) return observatoriesStore;
  const url = `${RESTEndpoint}/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`;
  const res = await (await fetch(url)).json();
  await observatoryPages.set(res.items);
}

export const aboutPages = writable(undefined);

async function getAboutPages(language = "en"): Promise<WagtailPage[]> {
  console.log("getAboutPages", { language });
  const aboutPagesStore = get(aboutPages);
  if (aboutPagesStore !== undefined) return aboutPagesStore;
  const url = `${RESTEndpoint}/pages/?order=title&type=wagtailcms.AboutIndexPage`;
  const res = await (await fetch(url)).json();
  const indexPageId = res.items[0].id;
  const pagesUrl = `${RESTEndpoint}/pages/?child_of=${indexPageId}`;
  const res_children = await (await fetch(pagesUrl)).json();
  await aboutPages.set(res_children.items);
  return res_children.items;
}

export const blogCategories = writable<BlogCategory[]>(undefined);
async function getBlogCategories(language = "en") {
  console.log("getBlogCategories", { language });
  const { data } = await client.query<{ blogcategories: BlogCategory[] }>({
    query: gql`
      query ($language: String) {
        blogcategories(language: $language) {
          id
          name
          slug
        }
      }
    `,
    variables: { language },
  });
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

export const user = writable<User>(undefined);
export const countries = writable<Country[]>([]);
export const regions = writable<Region[]>([]);
export const formfields = writable<FormFields>(undefined);

async function getBasics() {
  console.log("getBasics");
  const userStore = get(user);
  if (userStore !== undefined) return userStore;
  const { data } = await client.query({
    query: gql`
      query {
        me {
          id
          full_name
          username
          initials
          is_authenticated
          is_impersonate
          role
          userregionalinfo {
            country {
              id
              name
            }
            region {
              id
              name
            }
          }
          groups {
            id
            name
          }
        }
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
  });
  await user.set(data.me);
  await countries.set(data.countries);
  await regions.set(data.regions);
  await formfields.set(data.formfields);
}

export const chartDescriptions = writable<{
  web_of_transnational_deals: string;
  dynamics_overview: string;
  produce_info_map: string;
}>(undefined);
async function getChartDescriptions(language = "en") {
  console.log("getChartDescriptions", { language });
  const { data } = await client.query({
    query: gql`
      query chart_descriptions($language: String) {
        chart_descriptions(language: $language) {
          web_of_transnational_deals
          dynamics_overview
          produce_info_map
        }
      }
    `,
  });
  await chartDescriptions.set(data.chart_descriptions);
}

export async function dispatchLogin(username: string, password: string) {
  const mutation = gql`
    mutation Login($username: String!, $password: String!) {
      login(username: $username, password: $password) {
        status
        error
        user {
          id
          full_name
          username
          initials
          is_authenticated
          is_impersonate
          role
          userregionalinfo {
            country {
              id
              name
            }
            region {
              id
              name
            }
          }
          groups {
            id
            name
          }
        }
      }
    }
  `;
  const variables = { username, password };
  const { data } = await client.mutate({ mutation, variables });
  if (data.login.status === true) {
    user.set(data.login.user);
  }
  return data.login;
}
export async function dispatchLogout() {
  const { data } = await client.mutate({
    mutation: gql`
      mutation {
        logout
      }
    `,
  });
  return data.logout;
}

export async function fetchBasis(lang = "en") {
  console.log("LANG", lang);
  await getObservatoryPages(lang);
  await getBlogCategories(lang);
  await getAboutPages(lang);
  await getChartDescriptions(lang);
  await getBasics();
}
