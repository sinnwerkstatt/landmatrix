import { get, writable } from "svelte/store";
import { gql, request } from "graphql-request";

import type { BlogCategory, ObservatoryPage, WagtailPage } from "$lib/types/wagtail";
import { GQLEndpoint, RESTEndpoint } from "$lib/index";

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
  const gqlres = await request(GQLEndpoint, query, variables);
  await blogCategories.set(gqlres.blogcategories);
  return gqlres.blogcategories;
}

export async function fetchBasis() {
  await getObservatoryPages();
  await getBlogCategories();
  await getAboutPages();
}
