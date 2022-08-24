<script lang="ts">
  import { _ } from "svelte-i18n";
  import { blogCategories } from "$lib/stores";
  import type { BlogCategory, BlogPage } from "$lib/types/wagtail";
  import TagIcon from "$components/icons/TagIcon.svelte";
  import PageTitle from "$components/PageTitle.svelte";

  // import { PageData } from "./$types";
  //
  // export let data: PageData;

  export let data: {
    page: BlogPage;
    category: string | null;
    tag: string | null;
    blogpages: BlogPage[];
  };

  let filteredBlogpages: BlogPage[];
  $: filteredBlogpages = data.category
    ? data.blogpages.filter((page) =>
        page.categories.map((c) => c.slug).includes(data.category)
      )
    : data.tag
    ? data.blogpages.filter((page) => page.tags.map((t) => t.slug).includes(data.tag))
    : data.blogpages;

  let blogCategoriesWithAll: BlogCategory[];
  $: blogCategoriesWithAll = [
    { id: -1, slug: null, name: "All categories" },
    ...$blogCategories,
  ];
</script>

<div>
  <PageTitle class="inline-flex items-center gap-2">
    <span>{$_(data.page.title)}</span>
    {#if data.tag}
      <small class="inline-flex items-center">
        <TagIcon class="h-6 w-6" />
        {data.tag}
      </small>
    {/if}
  </PageTitle>

  <div class="mb-4 text-center">
    <ul class="flex flex-wrap justify-center">
      {#each blogCategoriesWithAll as cat}
        <li>
          <a
            href={cat.slug ? `?category=${cat.slug}` : "/resources"}
            class="block px-4 py-2 whitespace-nowrap {data.category === cat.slug
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
