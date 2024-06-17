<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import DataSourcesEdit from "$components/Data/DataSources/Edit.svelte"

  export let investor: InvestorHull
</script>

<DataSourcesEdit bind:version={investor.selected_version} />
