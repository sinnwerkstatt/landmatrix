<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { pageQuery } from "$lib/queries";

  export const load: Load = async ({ url }) => {
    const page = await pageQuery(url);

    return { props: { page } };
  };
</script>

<script lang="ts">
  import type { BlogPage } from "$lib/types/wagtail";
  import PageTitle from "$components/PageTitle.svelte";
  import Streamfield from "$components/Streamfield.svelte";

  export let page: BlogPage;
</script>

<div>
  <PageTitle>{page.title}</PageTitle>

  <div class="container mx-auto">
    <div class="meta mb-3">
      <div class="inline-block mr-4">
        <i class="far fa-calendar-alt" />
        {page.date}
      </div>
      {#if page.tags?.length > 0}
        <div class="inline-block">
          {#each page.tags as tag}
            <a href="/resources/?tag={tag.slug}">
              <!-- <Tag />-->
              {tag.name}
            </a>
          {/each}
        </div>
      {/if}
    </div>
    <Streamfield content={page.body} />
  </div>
</div>
