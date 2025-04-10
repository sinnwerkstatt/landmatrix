<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import { type SortBy } from "$lib/data/buckets"
  import { dealChoices } from "$lib/fieldChoices"
  import { filters } from "$lib/filters"
  import { dealsNG } from "$lib/stores"
  import { observatoryPages } from "$lib/stores/wagtail"
  import type { CountryOrRegion } from "$lib/types/wagtail"
  import { sum } from "$lib/utils/dataProcessing"

  import {
    getImplementationBuckets,
    getNegotiationBuckets,
    getProduce,
  } from "$components/Data/contextBar.svelte"
  import DealDisplayToggle from "$components/DealDisplayToggle.svelte"
  import { displayDealsCount } from "$components/Map/mapHelper"
  import StatusBarChart from "$components/StatusBarChart.svelte"

  import ContextBarContainer from "./ContextBarContainer.svelte"

  let deals = $derived($dealsNG.map(d => d.selected_version))

  let currentItem: CountryOrRegion | undefined = $derived.by(() => {
    let _currentItem: CountryOrRegion | undefined
    if (!$filters.region_id && !$filters.country_id) {
      _currentItem = {
        name: "Global",
        observatory_page: $observatoryPages.find(o => !o.country && !o.region),
      } as unknown as CountryOrRegion
    } else {
      _currentItem = {
        ...($filters.region_id
          ? page.data.regions.find(r => r.id === $filters.region_id)
          : page.data.countries.find(c => c.id === $filters.country_id)),
      } as CountryOrRegion
      _currentItem.observatory_page = $observatoryPages.find(
        o => o.id === _currentItem!.observatory_page_id,
      )
    }
    return _currentItem
  })

  let sortBy: SortBy = $derived($displayDealsCount ? "count" : "size")

  let chartNegStat = $derived(
    getNegotiationBuckets(
      deals,
      $dealChoices.negotiation_status_group,
      sortBy === "size",
    ),
  )
  let chartImpStat = $derived(
    getImplementationBuckets(
      deals,
      $dealChoices.implementation_status,
      sortBy === "size",
    ),
  )
  let chartProd = $derived(
    getProduce(deals, $dealChoices.produce_group, sortBy === "size"),
  )

  let totalCount = $derived(
    $displayDealsCount
      ? `${Math.round(deals.length).toLocaleString("fr").replace(",", ".")}`
      : `${Math.round(sum(deals, "deal_size")).toLocaleString("fr").replace(",", ".")} ${$_("ha")}`,
  )
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
        {#key chartNegStat}
          <StatusBarChart data={chartNegStat} width={400} />
        {/key}
      </div>
      <div class="mb-6 w-full">
        <h5 class="mb-3 text-center text-lg font-bold">
          {$_("Implementation status")}
        </h5>
        {#key chartImpStat}
          <StatusBarChart data={chartImpStat} width={400} />
        {/key}
      </div>
      <div class="mb-6 w-full">
        <h5 class="mb-3 text-center text-lg font-bold">{$_("Produce")}</h5>
        {#key chartProd}
          <StatusBarChart data={chartProd} width={400} />
        {/key}
      </div>
    </div>
  {/if}
</ContextBarContainer>
