<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { SortBy } from "$lib/data/buckets"
  import { createImplementationStatusChartData } from "$lib/data/charts/implementationStatus"
  import { createNegotiationStatusChartData } from "$lib/data/charts/negotiationStatusGroup"
  import { createProduceGroupChartData } from "$lib/data/charts/produceGroup"
  import { filters } from "$lib/filters"
  import { countries, dealsNG, regions } from "$lib/stores"
  import { observatoryPages } from "$lib/stores/wagtail"
  import type { CountryOrRegion } from "$lib/types/wagtail"
  import { sum } from "$lib/utils/data_processing"

  import DealDisplayToggle from "$components/DealDisplayToggle.svelte"
  import { displayDealsCount } from "$components/Map/map_helper"
  import StatusPieChart from "$components/StatusPieChart.svelte"

  import ContextBarContainer from "./ContextBarContainer.svelte"

  let currentItem: CountryOrRegion
  $: if (!$filters.region_id && !$filters.country_id) {
    currentItem = {
      name: "Global",
      observatory_page: $observatoryPages.find(o => !o.country && !o.region),
    } as CountryOrRegion
  } else {
    currentItem = {
      ...($filters.region_id
        ? $regions.find(r => r.id === $filters.region_id)
        : $countries.find(c => c.id === $filters.country_id)),
    } as CountryOrRegion
    currentItem.observatory_page = $observatoryPages.find(
      o => o.id === currentItem.observatory_page_id,
    )
  }

  let unit: "deals" | "ha"
  let sortBy: SortBy
  $: unit = $displayDealsCount ? "deals" : "ha"
  $: sortBy = $displayDealsCount ? "count" : "size"

  $: chartNegStat = createNegotiationStatusChartData($dealsNG, sortBy)
  $: chartImpStat = createImplementationStatusChartData($dealsNG, sortBy)
  $: chartProd = createProduceGroupChartData($dealsNG, sortBy)

  $: totalCount = $displayDealsCount
    ? `${Math.round($dealsNG.length).toLocaleString("fr")}`
    : `${Math.round(sum($dealsNG, "deal_size")).toLocaleString("fr")} ha`
</script>

<ContextBarContainer>
  {#if currentItem}
    <h2 class="heading5">{currentItem.name}</h2>
    {#if currentItem?.observatory_page}
      <p class="mb-1">
        {currentItem.observatory_page.short_description}
        <br />
        <a href="/observatory/{currentItem.observatory_page.meta.slug}/">
          {$_("Read more")}
        </a>
      </p>
    {/if}
  {/if}
  {#if $dealsNG.length}
    <div>
      <DealDisplayToggle />
      <div class="my-3 w-full text-center font-bold">
        {totalCount}
      </div>
      <div class="mb-6 w-full">
        <h5 class="mb-3 text-center text-lg font-bold">{$_("Negotiation status")}</h5>
        <StatusPieChart data={chartNegStat} {unit} />
      </div>
      <div class="mb-6 w-full">
        <h5 class="mb-3 text-center text-lg font-bold">
          {$_("Implementation status")}
        </h5>
        <StatusPieChart data={chartImpStat} {unit} />
      </div>
      <div class="mb-6 w-full">
        <h5 class="mb-3 text-center text-lg font-bold">{$_("Produce")}</h5>
        <StatusPieChart data={chartProd} {unit} />
      </div>
    </div>
  {/if}
</ContextBarContainer>
