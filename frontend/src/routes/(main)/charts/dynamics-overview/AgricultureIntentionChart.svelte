<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dealChoices, type ValueLabelEntry } from "$lib/fieldChoices"
  import { type DealVersion2 } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"
  import type { DataType } from "$components/StatusBarChart.svelte"

  interface Props {
    deals?: DealVersion2[]
    displayDealsCount?: boolean
  }

  let { deals = [], displayDealsCount = false }: Props = $props()

  const agricultureIntentions = [
    "BIOFUELS",
    "BIOMASS_ENERGY_GENERATION",
    "FODDER",
    "FOOD_CROPS",
    "LIVESTOCK",
    "NON_FOOD_AGRICULTURE",
    "AGRICULTURE_UNSPECIFIED",
  ] as const
  type AgricultureIntention = (typeof agricultureIntentions)[number]

  function createData(
    dls: DealVersion2[],
    groups: ValueLabelEntry[],
    bySize: boolean,
  ): DataType[] {
    const vBuckets = groups.map(group => ({
      _id: group.value,
      name: group.label,
      count: 0,
      size: 0,
      fillColor: {
        BIOFUELS: "hsl(50, 78%, 38%)", // "text-yellow-700",
        BIOMASS_ENERGY_GENERATION: "hsl(50, 78%, 48%)", // "text-yellow-600",
        FODDER: "hsl(50, 78%, 58%)", // "text-yellow-500",
        FOOD_CROPS: "hsl(50, 77%, 62%)", // "text-yellow-400",
        LIVESTOCK: "hsl(50, 77%, 71%)", // "text-yellow-300",
        NON_FOOD_AGRICULTURE: "hsl(51, 78%, 79%)", // "text-yellow-200",
        AGRICULTURE_UNSPECIFIED: "hsl(50, 78%, 87%)", // "text-yellow-100",
      }[group.value as AgricultureIntention],
    }))

    let totalCount = 0
    let totalSize = 0
    for (const deal of dls) {
      totalCount += 1
      totalSize += deal.deal_size ?? 0

      for (const intention of deal.current_intention_of_investment) {
        if (agricultureIntentions.includes(intention)) {
          let vbuck = vBuckets.find(x => x._id === intention)!
          vbuck.count += 1
          vbuck.size += deal.deal_size ?? 0
        }
      }
    }

    if (bySize) {
      return vBuckets
        .filter(n => n.size > 0)
        .map(n => ({
          name: n.name,
          value: ((n.size / totalSize) * 100).toFixed(),
          label: `<strong>${n.name}</strong>: ${n.size.toLocaleString("fr").replace(",", ".")} ${$_("ha")}`,
          fillColor: n.fillColor,
        }))
    } else {
      return vBuckets
        .filter(n => n.count > 0)
        .map(n => ({
          name: n.name,
          value: ((n.count / totalCount) * 100).toFixed(),
          label: `<strong>${n.name}</strong>: ${n.count.toFixed()} ${$_("deals")}`,
          fillColor: n.fillColor,
        }))
    }
  }

  let data = $derived(
    createData(
      deals,
      $dealChoices.intention_of_investment.filter(i => i.group === "AGRICULTURE"),
      !displayDealsCount,
    ),
  )
</script>

{#key data}
  <DownloadablePieChart title={$_("Investment in agriculture")} {data} />
{/key}
