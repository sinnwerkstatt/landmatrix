<script lang="ts">
  import type { WagtailPage } from "$lib/types/wagtail"

  import NewFooter from "$components/NewFooter.svelte"
  import PageTitle from "$components/PageTitle.svelte"
  import Streamfield from "$components/Streamfield.svelte"

  export let page: WagtailPage
</script>

<div class="flex min-h-full flex-col">
  <div class="px-2 pb-12">
    <PageTitle>{page.title}</PageTitle>
    <Streamfield content={page.body} />
  </div>
  <div class="flex-grow" />
  <NewFooter />
</div>
