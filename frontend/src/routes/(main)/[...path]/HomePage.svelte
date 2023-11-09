<script lang="ts">
  import type { WagtailPage } from "$lib/types/wagtail"

  import Streamfield from "$components/StreamfieldHomepage.svelte"
  import NewFooter from "$components/NewFooter.svelte"

  export let page: WagtailPage
</script>

<div class="w-full">
  <Streamfield content={page.body} />
</div>
<NewFooter />
