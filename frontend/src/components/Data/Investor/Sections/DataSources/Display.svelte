<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import DataSourcesDisplay from "$components/Data/DataSources/Display.svelte"

  export let investor: InvestorHull
</script>

<DataSourcesDisplay version={investor.selected_version} />
