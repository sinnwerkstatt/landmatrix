<script lang="ts">
  import type { WagtailPage } from "$lib/types/wagtail"

  import NewFooter from "$components/NewFooter.svelte"
  import Streamfield from "$components/StreamfieldHomepage.svelte"

  interface Props {
    page: WagtailPage
  }

  let { page }: Props = $props()
</script>

<div class="w-full">
  <Streamfield content={page.body} />
  <NewFooter />
</div>
