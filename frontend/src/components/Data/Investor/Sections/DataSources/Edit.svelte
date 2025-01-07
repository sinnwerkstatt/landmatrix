<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import DataSourcesEdit from "$components/Data/DataSources/Edit.svelte"

  interface Props {
    investor: InvestorHull;
  }

  let { investor = $bindable() }: Props = $props();
</script>

<DataSourcesEdit bind:version={investor.selected_version} />
