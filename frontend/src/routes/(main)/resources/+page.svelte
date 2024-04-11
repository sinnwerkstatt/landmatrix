<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { components } from "$lib/openAPI"
  import { blogCategories } from "$lib/stores"
  import type { BlogCategory } from "$lib/types/wagtail"

  import TagIcon from "$components/icons/TagIcon.svelte"
  import NewFooter from "$components/NewFooter.svelte"
  import PageTitle from "$components/PageTitle.svelte"

  export let data

  $: blogpages = data.blogpages

  let filteredBlogPages: components["schemas"]["BlogPage"][]
  $: filteredBlogPages = data.category
    ? $blogpages.filter(bp => bp.categories.map(c => c.slug).includes(data.category))
    : data.tag
      ? $blogpages.filter(bp => bp.tags.map(t => t.slug).includes(data.tag))
      : $blogpages

  let blogCategoriesWithAll: BlogCategory[]
  $: blogCategoriesWithAll = [
    { id: -1, slug: null, name: $_("All") },
    ...$blogCategories.sort((a, b) => a.id - b.id),
  ]
</script>

<div class="flex min-h-full flex-col">
  <PageTitle class="inline-flex items-center gap-2">
    <span>{data.page.title}</span>
    {#if data.tag}
      <small class="inline-flex items-center">
        <TagIcon class="h-6 w-6" />
        {data.tag}
      </small>
    {/if}
  </PageTitle>

  <div class="mb-12 mt-8 text-center">
    <ul class="flex flex-wrap justify-center gap-1">
      {#each blogCategoriesWithAll as cat}
        <li>
          <a
            href={cat.slug ? `?category=${cat.slug}` : "/resources/"}
            class="button1 mx-1 block w-fit whitespace-nowrap rounded border border-orange px-3 py-2 shadow transition hover:border-orange-700 {data.category ===
            cat.slug
              ? 'bg-orange font-bold text-white hover:bg-orange-700 hover:text-white'
              : 'hover:text-orange-700 '}"
          >
            {cat.name}
          </a>
        </li>
      {/each}
    </ul>
  </div>

  <div class="container mx-auto grid gap-4 px-10 pb-5 md:grid-cols-2 lg:grid-cols-3">
    {#each filteredBlogPages as blogpage}
      <div class="col-md-6 col-lg-4 mb-3">
        <div
          class="h-full rounded border border-gray-900 bg-gray-50 dark:border-white dark:bg-gray-800"
        >
          {#if blogpage.header_image}
            <img
              src={blogpage.header_image.url}
              class="w-full rounded-t object-cover"
              alt=""
              loading="lazy"
            />
          {/if}
          <div class="p-2">
            <h5 class="heading5 mb-4">
              <a
                href={blogpage.url}
                class=" text-gray-900 hover:text-orange dark:text-white"
              >
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

  <div class="flex-grow" />
  <NewFooter />
</div>
