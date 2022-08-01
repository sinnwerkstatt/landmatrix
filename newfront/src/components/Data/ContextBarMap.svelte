<script lang="ts">
  import { _ } from "svelte-i18n";
  import { deals } from "$lib/data";
  import { filters } from "$lib/filters";
  import { countries, observatoryPages, regions } from "$lib/stores";
  import type { CountryOrRegion } from "$lib/types/wagtail";
  import { sum } from "$lib/utils/data_processing";
  import DealDisplayToggle from "$components/DealDisplayToggle.svelte";
  import { displayDealsCount } from "$components/Map/map_helper";
  import StatusPieChart from "$components/StatusPieChart.svelte";
  import ContextBarContainer from "./ContextBarContainer.svelte";
  import {
    calcImplementationStatusChart,
    calcNegotiationStatusChart,
    calcProduceChart,
  } from "./contextBarMapCharts";

  let currentItem: CountryOrRegion;
  $: if (!$filters.region_id && !$filters.country_id) {
    currentItem = {
      name: "Global",
      observatory_page: $observatoryPages.find((o) => !o.country && !o.region),
    };
  } else {
    currentItem = {
      ...($filters.region_id
        ? $regions.find((r) => r.id === $filters.region_id)
        : $countries.find((c) => c.id === $filters.country_id)),
    };
    currentItem.observatory_page = $observatoryPages.find(
      (o) => o.id === currentItem.observatory_page_id
    );
  }

  $: chartNegStat = calcNegotiationStatusChart($deals, $displayDealsCount);
  $: chartImpStat = calcImplementationStatusChart($deals, $displayDealsCount);
  $: chartProd = calcProduceChart($deals);

  $: totalCount = $displayDealsCount
    ? `${Math.round($deals?.length).toLocaleString("fr")}`
    : `${Math.round(sum($deals, "deal_size")).toLocaleString("fr")} ha`;
</script>

<ContextBarContainer>
  {#if currentItem}
    <h2 class="font-bold text-lg my-3 leading-5">{currentItem.name}</h2>
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
  {#if $deals?.length}
    <div>
      <DealDisplayToggle />
      <div class="w-full text-center font-bold my-3">
        {totalCount}
      </div>
      <div class="w-full mb-3">
        <h5 class="text-left text-lg mt-4">{$_("Negotiation status")}</h5>
        <StatusPieChart
          data={chartNegStat}
          unit={$displayDealsCount ? "deals" : "ha"}
        />
      </div>
      <div class="w-full mb-3">
        <h5 class="text-left text-lg mt-4">{$_("Implementation status")}</h5>
        <StatusPieChart
          data={chartImpStat}
          unit={$displayDealsCount ? "deals" : "ha"}
        />
      </div>
      <div class="w-full mb-3">
        <h5 class="text-left text-lg mt-4">{$_("Produce")}</h5>
        <StatusPieChart data={chartProd} unit="%" />
      </div>
    </div>
  {/if}
</ContextBarContainer>
