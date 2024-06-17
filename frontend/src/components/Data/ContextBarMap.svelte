<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { SortBy } from "$lib/data/buckets"
  import {
    getImplementationStatusColor,
    implementationStatusReducer,
  } from "$lib/data/charts/implementationStatus"
  import {
    createNegotiationStatusGroupReducer,
    getNegotiationStatusGroupColor,
    type NegStatGroupMap,
  } from "$lib/data/charts/negotiationStatusGroup"
  import {
    getProduceGroupColor,
    produceGroupReducer,
  } from "$lib/data/charts/produceGroup"
  import { createChartData } from "$lib/data/createChartData"
  import { filters } from "$lib/filters"
  import { dealsNG, fieldChoices } from "$lib/stores"
  import { observatoryPages } from "$lib/stores/wagtail"
  import {
    NegotiationStatusGroup,
    ProduceGroup,
    type ImplementationStatus,
  } from "$lib/types/data"
  import type { CountryOrRegion } from "$lib/types/wagtail"
  import { sum } from "$lib/utils/dataProcessing"

  import DealDisplayToggle from "$components/DealDisplayToggle.svelte"
  import { displayDealsCount } from "$components/Map/map_helper"
  import StatusPieChart from "$components/StatusPieChart.svelte"

  import ContextBarContainer from "./ContextBarContainer.svelte"

  $: deals = $dealsNG.map(d => d.selected_version)

  let currentItem: CountryOrRegion
  $: if (!$filters.region_id && !$filters.country_id) {
    currentItem = {
      name: "Global",
      observatory_page: $observatoryPages.find(o => !o.country && !o.region),
    } as unknown as CountryOrRegion
  } else {
    currentItem = {
      ...($filters.region_id
        ? $page.data.regions.find(r => r.id === $filters.region_id)
        : $page.data.countries.find(c => c.id === $filters.country_id)),
    } as CountryOrRegion
    currentItem.observatory_page = $observatoryPages.find(
      o => o.id === currentItem.observatory_page_id,
    )
  }

  let unit: "deals" | "ha"
  let sortBy: SortBy
  $: unit = $displayDealsCount ? "deals" : "ha"
  $: sortBy = $displayDealsCount ? "count" : "size"

  $: negStatGroupMap = $fieldChoices["deal"]["negotiation_status"].reduce(
    (acc, { value, group }) => ({ ...acc, [value]: group }),
    {},
  ) as NegStatGroupMap
  $: negStatGroupLabels = $fieldChoices["deal"]["negotiation_status_group"].reduce(
    (acc, { value, label }) => ({ ...acc, [value]: label }),
    {},
  ) as { [key in NegotiationStatusGroup]: string }

  $: chartNegStat = createChartData(
    createNegotiationStatusGroupReducer(negStatGroupMap),
    Object.values(NegotiationStatusGroup),
    (key: NegotiationStatusGroup) => negStatGroupLabels[key],
    getNegotiationStatusGroupColor,
  )(deals, sortBy)

  $: impStatLabels = $fieldChoices["deal"]["implementation_status"].reduce(
    (acc, { value, label }) => ({ ...acc, [value]: label }),
    {},
  ) as { [key in ImplementationStatus]: string }

  $: chartImpStat = createChartData<ImplementationStatus>(
    implementationStatusReducer,
    $fieldChoices["deal"]["implementation_status"].map(
      x => x.value,
    ) as ImplementationStatus[],
    (key: ImplementationStatus) => impStatLabels[key],
    getImplementationStatusColor,
  )(deals, sortBy)

  $: produceGroupLabels = $fieldChoices["deal"]["produce_group"].reduce(
    (acc, { value, label }) => ({ ...acc, [value]: label }),
    {},
  ) as { [key in ProduceGroup]: string }

  $: chartProd = createChartData<ProduceGroup>(
    produceGroupReducer,
    Object.values(ProduceGroup),
    (produceGroup: ProduceGroup) => produceGroupLabels[produceGroup],
    getProduceGroupColor,
  )(deals, sortBy)

  $: totalCount = $displayDealsCount
    ? `${Math.round(deals.length).toLocaleString("fr").replace(",", ".")}`
    : `${Math.round(sum(deals, "deal_size")).toLocaleString("fr").replace(",", ".")} ha`
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
  {#if deals.length}
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
