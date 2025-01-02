<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dealChoices } from "$lib/fieldChoices"
  import { type DealVersion2 } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"
  import { getNegotiationBuckets } from "$components/Data/contextBar.svelte"

  interface Props {
    deals?: DealVersion2[]
    displayDealsCount?: boolean
  }

  let { deals = [], displayDealsCount = false }: Props = $props()

  let data = $derived(
    getNegotiationBuckets(
      deals,
      $dealChoices.negotiation_status_group,
      !displayDealsCount,
    ),
  )
</script>

{#key data}
  <DownloadablePieChart title={$_("Negotiation status")} {data} />
{/key}
