<script lang="ts">
  import type { BlogPage } from "$lib/types/wagtail";
  import PageTitle from "$components/PageTitle.svelte";
  import Streamfield from "$components/Streamfield.svelte";

  // import type { PageData } from "./$types";
  //
  // export let data: PageData;
  export let data: { page: BlogPage };
</script>

<div>
  <PageTitle>{data.page.title}</PageTitle>

  <div class="container mx-auto px-10">
    <div class="meta mb-3">
      <div class="mr-4 inline-block">
        <i class="far fa-calendar-alt" />
        {data.page.date}
      </div>
      {#if data.page.tags?.length > 0}
        <div class="inline-block">
          {#each data.page.tags as tag}
            <a href="/resources/?tag={tag.slug}">
              <!-- <Tag />-->
              {tag.name}
            </a>
          {/each}
        </div>
      {/if}
    </div>
    <Streamfield content={data.page.body} />
  </div>
</div>
