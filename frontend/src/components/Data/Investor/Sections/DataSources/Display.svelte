<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import DataSourcesDisplay from "$components/Data/DataSources/Display.svelte"

  interface Props {
    investor: InvestorHull
  }

  let { investor }: Props = $props()
</script>

<DataSourcesDisplay version={investor.selected_version} model="investor" />
