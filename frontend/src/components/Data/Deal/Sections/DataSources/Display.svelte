<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import DataSourcesDisplay from "$components/Data/DataSources/Display.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal }: Props = $props()
</script>

<DataSourcesDisplay version={deal.selected_version} model="deal" />
