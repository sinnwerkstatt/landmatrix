<script lang="ts">
  import type { MutableInvestorHull } from "$lib/types/data"

  import DataSourcesEdit from "$components/Data/DataSources/Edit.svelte"

  interface Props {
    investor: MutableInvestorHull
  }

  let { investor = $bindable() }: Props = $props()
</script>

<DataSourcesEdit model="investor" bind:version={investor.selected_version} />
