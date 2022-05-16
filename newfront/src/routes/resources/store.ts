import { gql } from "@apollo/client/core";
import { get, writable } from "svelte/store";
import { client } from "$lib/apolloClient";
import type { BlogPage } from "$lib/types/wagtail";

const blogpages = writable<BlogPage[]>(undefined);

export async function getBlogPages(language = "en"): Promise<BlogPage[]> {
  console.log("getBlogPages", { language });
  const blogpagesStore = get(blogpages);
  if (blogpagesStore !== undefined) return blogpagesStore;

  const blogpages_query = gql`
    query {
      blogpages {
        id
        title
        slug
        date
        header_image
        excerpt
        categories {
          slug
        }
        tags {
          slug
        }
        url
      }
    }
  `;
  const { data } = await client.query<{ blogpages: BlogPage[] }>({
    query: blogpages_query,
  });
  await blogpages.set(data.blogpages);
  return data.blogpages;
}
