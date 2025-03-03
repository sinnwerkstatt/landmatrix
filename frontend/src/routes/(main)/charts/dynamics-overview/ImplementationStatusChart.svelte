<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dealChoices } from "$lib/fieldChoices"
  import type { DealVersion } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"
  import { getImplementationBuckets } from "$components/Data/contextBar.svelte"

  interface Props {
    deals?: DealVersion[]
    displayDealsCount?: boolean
  }

  let { deals = [], displayDealsCount = false }: Props = $props()

  let data = $derived(
    getImplementationBuckets(
      deals,
      $dealChoices.implementation_status,
      !displayDealsCount,
    ),
  )
</script>

{#key data}
  <DownloadablePieChart {data} title={$_("Implementation status")} />
{/key}
