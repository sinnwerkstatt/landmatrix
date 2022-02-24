import { get, writable } from "svelte/store";
import { gql, request } from "graphql-request";

import type { BlogCategory, ObservatoryPage, WagtailPage } from "$lib/types/wagtail";
import { GQLEndpoint } from "$lib/index";

export const observatoryPages = writable(undefined);
export async function getObservatoryPages(language = "en"): Promise<ObservatoryPage[]> {
  console.log("getObservatoryPages", { language });
  const observatoriesStore = get(observatoryPages);
  if (observatoriesStore !== undefined) return observatoriesStore;
  const url = `http://localhost:8000/wagtailapi/v2/pages/?order=title&type=wagtailcms.ObservatoryPage&fields=region,country,short_description`;
  const res = await (await fetch(url)).json();
  console.log(res);
  await observatoryPages.set(res.items);
  return res.items;
}

export const aboutPages = writable(undefined);
export async function getAboutPages(language = "en"): Promise<WagtailPage[]> {
  console.log("getAboutPages", { language });
  const aboutPagesStore = get(aboutPages);
  if (aboutPagesStore !== undefined) return aboutPagesStore;
  const url = `http://localhost:8000/wagtailapi/v2/pages/?order=title&type=wagtailcms.AboutIndexPage`;
  const res = await (await fetch(url)).json();
  const indexPageId = res.items[0].id;
  const pagesUrl = `http://localhost:8000/wagtailapi/v2/pages/?child_of=${indexPageId}`;
  const res_children = await (await fetch(pagesUrl)).json();
  await aboutPages.set(res_children.items);
  return res_children.items;
}

export const blogCategories = writable(undefined);
export async function getBlogCategories(language = "en"): Promise<BlogCategory[]> {
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
  console.log(gqlres);
  await blogCategories.set(gqlres.blogcategories);
  return gqlres.blogcategories;
}
