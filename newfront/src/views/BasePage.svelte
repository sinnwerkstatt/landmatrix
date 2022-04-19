<script lang="ts">
  import type { WagtailPage } from "$lib/types/wagtail";
  import PageTitle from "$components/PageTitle.svelte";
  import Streamfield from "$components/Streamfield.svelte";

  export let page: WagtailPage;
</script>

<PageTitle>
  {page.title}
</PageTitle>
<Streamfield content={page.body} />
