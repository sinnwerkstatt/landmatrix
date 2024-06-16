<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import SectionDataSources from "$components/SectionDataSources.svelte"

  export let investor: InvestorHull
</script>

<SectionDataSources version={investor.selected_version} />
