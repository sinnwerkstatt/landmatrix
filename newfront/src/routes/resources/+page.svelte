<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";
  import { gql } from "@urql/svelte";
  import { pageQuery } from "$lib/queries";

  export const load: Load = async ({ url, fetch, stuff }) => {
    const page = await pageQuery(url, fetch);
    const { data } = await stuff.urqlClient
      .query(
        gql`
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
        `
      )
      .toPromise();
    const category = url.searchParams.get("category");
    const tag = url.searchParams.get("tag");
    return { props: { page, blogpages: data.blogpages, category, tag } };
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import { blogCategories } from "$lib/stores";
  import type { BlogCategory, BlogPage, WagtailPage } from "$lib/types/wagtail";
  import TagIcon from "$components/icons/TagIcon.svelte";
  import PageTitle from "$components/PageTitle.svelte";

  export let page: WagtailPage;
  export let blogpages: BlogPage[] = [];
  export let category: string;
  export let tag: string;

  let filteredBlogpages: BlogPage[];
  $: filteredBlogpages = category
    ? blogpages.filter((page) => page.categories.map((c) => c.slug).includes(category))
    : tag
    ? blogpages.filter((page) => page.tags.map((t) => t.slug).includes(tag))
    : blogpages;

  let blogCategoriesWithAll: BlogCategory[];
  $: blogCategoriesWithAll = [
    { id: -1, slug: null, name: "All categories" },
    ...$blogCategories,
  ];
</script>

<div>
  <PageTitle class="inline-flex items-center gap-2">
    <span>{$_(page.title)}</span>
    {#if tag}
      <small class="inline-flex items-center">
        <TagIcon class="h-6 w-6" />
        {tag}
      </small>
    {/if}
  </PageTitle>

  <div class="mb-4 text-center">
    <ul class="flex flex-wrap justify-center">
      {#each blogCategoriesWithAll as cat}
        <li>
          <a
            href={cat.slug ? `?category=${cat.slug}` : "/resources"}
            class="block px-4 py-2 whitespace-nowrap {category === cat.slug
              ? 'text-white bg-orange'
              : ''}"
          >
            {$_(cat.name)}
          </a>
        </li>
      {/each}
    </ul>
  </div>
  <div class="container mx-auto px-10 grid md:grid-cols-2 lg:grid-cols-3 gap-4">
    {#each filteredBlogpages as blogpage}
      <div class="col-md-6 col-lg-4 mb-3">
        <div class="border border-black/20 rounded">
          {#if blogpage.header_image}
            <img loading="lazy" src={blogpage.header_image} class="rounded-t" alt="" />
          {/if}
          <div class="p-2">
            <h5 class="text-lg font-bold mb-4">
              <a href={blogpage.url} class="text-lm-dark">
                {blogpage.title}
              </a>
            </h5>
            <p>{@html blogpage.excerpt}</p>

            <small class="text-gray-500">{blogpage.date}</small>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>
