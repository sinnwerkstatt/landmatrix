import { gql, GraphQLClient } from "graphql-request";
import { get, writable } from "svelte/store";
import type { User } from "$lib/types/user";
import type {
  BlogCategory,
  Country,
  ObservatoryPage,
  Region,
  WagtailPage,
} from "$lib/types/wagtail";
import { GQLEndpoint, RESTEndpoint } from "./index";

const graphQLClient = new GraphQLClient(GQLEndpoint, {
  credentials: "include",
  mode: "cors",
});

export const observatoryPages = writable(undefined);

async function getObservatoryPages(language = "en"): Promise<ObservatoryPage[]> {
  console.log("getObservatoryPages", { language });
  const observatoriesStore = get(observatoryPages);
  if (observatoriesStore !== undefined) return observatoriesStore;
  const url = `${RESTEndpoint}/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`;
  const res = await (await fetch(url)).json();
  await observatoryPages.set(res.items);
  return res.items;
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

export const blogCategories = writable(undefined);

async function getBlogCategories(language = "en"): Promise<BlogCategory[]> {
  console.log("getBlogCategories", { language });
  const blogcategoriesStore = get(blogCategories);
  if (blogcategoriesStore !== undefined) return blogcategoriesStore;
  const query = gql`
    query ($language: String) {
      blogcategories(language: $language) {
        id
        name
        slug
      }
    }
  `;
  const variables = { language };
  const gqlres = await graphQLClient.request(query, variables);
  await blogCategories.set(gqlres.blogcategories);
  return gqlres.blogcategories;
}

export const user = writable(undefined as User);
export const countries = writable([] as Country[]);
export const regions = writable([] as Region[]);
export const formfields = writable([]);

async function getBasics(): Promise<User> {
  console.log("getBasics");
  const userStore = get(user);
  if (userStore !== undefined) return userStore;
  const query = gql`
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
  `;
  const gqlres = await graphQLClient.request(query);
  await user.set(gqlres.me);
  await countries.set(gqlres.countries);
  await regions.set(gqlres.regions);
  await formfields.set(gqlres.formfields);
}

export async function dispatchLogin(username, password) {
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
  const data = await graphQLClient.request(mutation, variables);
  if (data.login.status === true) {
    user.set(data.login.user);
  }
  return data.login;
}
export async function dispatchLogout() {
  const mutation = gql`
    mutation {
      logout
    }
  `;
  const data = await graphQLClient.request(mutation);
  return data.logout;
}

export async function fetchBasis(lang = "en") {
  console.log("LANG", lang);
  await getObservatoryPages(lang);
  await getBlogCategories(lang);
  await getAboutPages(lang);
  await getBasics();
}
