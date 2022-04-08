import { gql, request } from "graphql-request";
import { get, writable } from "svelte/store";
import { GQLEndpoint } from "$lib";
import type { BlogPage } from "$lib/types/wagtail";

const blogpages = writable(undefined);

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
  const res = await request(GQLEndpoint, blogpages_query);
  await blogpages.set(res.blogpages);
  return res.blogpages;
}
