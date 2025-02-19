<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import DataSourcesEdit from "$components/Data/DataSources/Edit.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal = $bindable() }: Props = $props()
</script>

<DataSourcesEdit model="deal" bind:version={deal.selected_version} />
