<script lang="ts">
  import type { WagtailPage } from "$lib/types/wagtail"

  import NewFooter from "$components/NewFooter.svelte"
  import Streamfield from "$components/StreamfieldHomepage.svelte"

  export let page: WagtailPage
</script>

<div class="w-full">
  <Streamfield content={page.body} />
  <NewFooter />
</div>
