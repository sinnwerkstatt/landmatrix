<script lang="ts">
  import type { WagtailPage } from "$lib/types/wagtail"

  import Streamfield from "$components/StreamfieldHomepage.svelte"

  export let page: WagtailPage
</script>

<div class="w-full">
  <Streamfield content={page.body} />
</div>
