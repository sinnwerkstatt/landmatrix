<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import DataSourcesDisplay from "$components/Data/DataSources/Display.svelte"

  export let deal: DealHull
</script>

<DataSourcesDisplay version={deal.selected_version} />
