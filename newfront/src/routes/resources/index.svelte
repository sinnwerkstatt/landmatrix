<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";
  import { pageQuery } from "$lib/queries";
  import { getBlogPages } from "./store";

  export const load: Load = async ({ url, fetch }) => {
    const page = await pageQuery(url, fetch);
    const blogpages = await getBlogPages();
    const category = url.searchParams.get("category");
    const tag = url.searchParams.get("tag");
    return { props: { page, blogpages, category, tag } };
  };
</script>

<script lang="ts">
  import PageTitle from "$components/PageTitle.svelte";
  import type { BlogCategory, BlogPage, WagtailPage } from "$lib/types/wagtail";
  import { blogCategories } from "$lib/stores";
  import { _ } from "svelte-i18n";

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
  <PageTitle>
    <span>{$_(page.title)}</span>
    {#if tag}
      <small><i class="fas fa-tags" /> {tag}</small>
    {/if}
  </PageTitle>

  <div class="mb-4 text-center">
    <ul class="flex flex-wrap justify-center">
      {#each blogCategoriesWithAll as cat}
        <li>
          <a
            class:activePill={category === cat.slug}
            href={cat.slug ? `?category=${cat.slug}` : "/resources"}
            class="block px-4 py-2 whitespace-nowrap"
          >
            {$_(cat.name)}
          </a>
        </li>
      {/each}
    </ul>
  </div>
  <div class="container mx-auto grid md:grid-cols-2 lg:grid-cols-3 gap-4">
    {#each filteredBlogpages as blogpage}
      <div class="col-md-6 col-lg-4 mb-3">
        <div class="border border-black/20 rounded">
          {#if blogpage.header_image}
            <img src={blogpage.header_image} class="rounded-t" alt="" />
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

<style>
  .activePill {
    @apply text-white bg-orange;
  }
</style>
