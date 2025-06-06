<script lang="ts">
  import { _ } from "svelte-i18n"

  import { createGroupMap, dealChoices, type ValueLabelEntry } from "$lib/fieldChoices"
  import {
    IntentionOfInvestmentGroup,
    type DealVersion,
    type IoIGroupMap,
  } from "$lib/types/data"

  import DownloadablePieChart from "$components/Data/Charts/DownloadablePieChart.svelte"
  import type { DataType } from "$components/StatusBarChart.svelte"

  interface Props {
    deals?: DealVersion[]
    displayDealsCount?: boolean
  }

  let { deals = [], displayDealsCount = false }: Props = $props()

  let ioiGroupMap = $derived(
    createGroupMap<IoIGroupMap>($dealChoices.intention_of_investment),
  )

  function createData(
    dls: DealVersion[],
    groups: ValueLabelEntry[],
    bySize: boolean,
  ): DataType[] {
    const vBuckets = groups.map(group => ({
      name: group.label,
      count: 0,
      size: 0,
      fillColor: {
        AGRICULTURE: "hsl(50, 78%, 58%)", // "text-yellow-500",
        FORESTRY: "hsl(94, 56%, 65%)", // "text-green-500",
        RENEWABLE_ENERGY: "hsl(233, 76%, 73%)", // "text-purple-400",
        OTHER: "hsl(0, 0%, 52%)", // "text-gray-400",
      }[group.value as "AGRICULTURE" | "FORESTRY" | "RENEWABLE_ENERGY" | "OTHER"],
    }))

    let totalCount = 0
    let totalSize = 0
    for (const deal of dls) {
      const intentions = deal.current_intention_of_investment ?? []
      const intentionGroups = intentions.map(intention => ioiGroupMap[intention])

      totalCount += 1
      totalSize += deal.deal_size ?? 0

      if (intentionGroups.includes(IntentionOfInvestmentGroup.AGRICULTURE)) {
        vBuckets[0].count += 1
        vBuckets[0].size += deal.deal_size ?? 0
      }
      if (intentionGroups.includes(IntentionOfInvestmentGroup.FORESTRY)) {
        vBuckets[1].count += 1
        vBuckets[1].size += deal.deal_size ?? 0
      }
      if (intentionGroups.includes(IntentionOfInvestmentGroup.RENEWABLE_ENERGY)) {
        vBuckets[2].count += 1
        vBuckets[2].size += deal.deal_size ?? 0
      }
      if (intentionGroups.includes(IntentionOfInvestmentGroup.OTHER)) {
        vBuckets[3].count += 1
        vBuckets[3].size += deal.deal_size ?? 0
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
    createData(deals, $dealChoices.intention_of_investment_group, !displayDealsCount),
  )
</script>

{#key data}
  <DownloadablePieChart title={$_("Intention of investment")} {data} />
{/key}
