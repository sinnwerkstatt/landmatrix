import { get, writable } from "svelte/store";
import { gql, GraphQLClient } from "graphql-request";

import { GQLEndpoint, RESTEndpoint } from "$lib/index";
import type { BlogCategory, ObservatoryPage, WagtailPage } from "$lib/types/wagtail";
import type { User } from "$lib/types/user";

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
  const variables = { language: "en" };
  const gqlres = await graphQLClient.request(query, variables);
  await blogCategories.set(gqlres.blogcategories);
  return gqlres.blogcategories;
}

export const user = writable(undefined);

async function getMe(): Promise<User> {
  console.log("getMe");
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
    }
  `;
  const gqlres = await graphQLClient.request(query);
  await user.set(gqlres.me);
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

export async function fetchBasis() {
  await getObservatoryPages();
  await getBlogCategories();
  await getAboutPages();
  await getMe();
}
