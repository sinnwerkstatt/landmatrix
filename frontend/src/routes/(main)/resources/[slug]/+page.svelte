<script lang="ts">
  import { _ } from "svelte-i18n"

  import FilePdfIcon from "$components/icons/FilePdfIcon.svelte"
  import NewFooter from "$components/NewFooter.svelte"
  import PageTitle from "$components/PageTitle.svelte"
  import Streamfield from "$components/Streamfield.svelte"
  import WagtailBird from "$components/Wagtail/WagtailBird.svelte"

  export let data
</script>

<div class="mb-10 flex flex-col xl:mb-16">
  <PageTitle>{data.page.title}</PageTitle>

  <div class="mx-auto w-[clamp(20rem,75%,56rem)]">
    <div class="mb-6 flex gap-4">
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
  </div>

  {#if data.page.documents.length}
    <div class="container mx-auto grid md:grid-cols-3">
      <Streamfield class="md:col-span-2" content={data.page.body} />

      <div class="max-w-[1200px] px-3 sm:px-6">
        <h2 class="heading4">{$_("Downloads")}</h2>
        <div class="flex flex-col gap-2">
          {#each data.page.documents as doc}
            {#if doc.type === "text"}
              <div>{doc.value}</div>
            {:else if doc.type === "document"}
              <a
                class="flex w-fit items-center gap-2 border border-orange-500 bg-orange-100 px-4 py-2 text-black hover:bg-orange-600 hover:text-white"
                href={doc.value.file}
                target="_blank"
              >
                <FilePdfIcon class="h-6 w-6" />
                {doc.value.title}
              </a>
            {/if}
          {/each}
        </div>
      </div>
    </div>
  {:else}
    <Streamfield class="md:col-span-2" content={data.page.body} />
  {/if}
</div>

<NewFooter />

{#if data.user?.is_superuser || data.user?.is_staff}
  <WagtailBird page={data.page} />
{/if}
