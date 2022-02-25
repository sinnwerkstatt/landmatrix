<script lang="ts">
  import Streamfield from "$components/Streamfield.svelte";
  import PageTitle from "$components/PageTitle.svelte";
  import type { WagtailPage } from "$lib/types/wagtail";

  export let page: WagtailPage;
</script>

<div class="mb-12">
  <PageTitle>
    {page.title}
  </PageTitle>
  <Streamfield content={page.body} />
</div>
