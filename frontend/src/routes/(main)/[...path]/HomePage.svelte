<script lang="ts">
  import type { WagtailPage } from "$lib/types/wagtail"

  import PageTitle from "$components/PageTitle.svelte"
  import Streamfield from "$components/StreamfieldHomepage.svelte"

  export let page: WagtailPage
</script>

<div class=" w-full pb-12">
  <Streamfield content={page.body} />
</div>
