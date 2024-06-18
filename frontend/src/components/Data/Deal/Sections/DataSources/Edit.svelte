<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import DataSourcesEdit from "$components/Data/DataSources/Edit.svelte"

  export let deal: DealHull
</script>

<DataSourcesEdit bind:version={deal.selected_version} />
