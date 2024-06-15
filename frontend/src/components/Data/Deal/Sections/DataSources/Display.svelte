<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import SectionDataSources from "$components/SectionDataSources.svelte"

  export let deal: DealHull
</script>

<SectionDataSources version={deal.selected_version} />
