<script lang="ts">
  import type { InvestorHull, Mutable } from "$lib/types/data"

  import DataSourcesEdit from "$components/Data/DataSources/Edit.svelte"

  interface Props {
    investor: Mutable<InvestorHull>
  }

  let { investor = $bindable() }: Props = $props()
</script>

<DataSourcesEdit model="investor" bind:version={investor.selected_version} />
