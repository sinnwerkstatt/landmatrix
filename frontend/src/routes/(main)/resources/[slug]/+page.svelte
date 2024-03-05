<script lang="ts">
  import NewFooter from "$components/NewFooter.svelte"
  import PageTitle from "$components/PageTitle.svelte"
  import Streamfield from "$components/Streamfield.svelte"

  export let data
</script>

<div class="flex min-h-full flex-col">
  <PageTitle>{data.page.title}</PageTitle>

  <div class="mx-auto mb-10 w-[clamp(20rem,75%,56rem)] xl:mb-16">
    <div class="mb-6 inline-flex gap-4">
      <span class="mr-4">{data.page.date}</span>
      {#if data.page.tags?.length > 0}
        {#each data.page.tags as tag}
          <a href="/resources/?tag={tag.slug}">
            <!-- <Tag />-->
            {tag.name}
          </a>
        {/each}
      {/if}
    </div>
    <Streamfield content={data.page.body} />
  </div>

  <div class="flex-grow" />
  <NewFooter />
</div>
