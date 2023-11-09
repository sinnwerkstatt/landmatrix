<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { countries, loading, regions } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"
  import type { Country, Region } from "$lib/types/wagtail"

  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"

  import type { Counts } from "./case_statistics"
  import QualityGoals from "./QualityGoals.svelte"
  import StatisticsTable from "./StatisticsTable.svelte"
  import TimespanChanges from "./TimespanChanges.svelte"

  let selCountry: Country | undefined
  let selRegion: Region | undefined

  let counts: Counts = {}
  let simpleDeals: Deal[] = []
  let simpleInvestors: Investor[] = []

  async function getCounts(region: Region | undefined, country: Country | undefined) {
    loading.set(true)

    let url = `/api/case_statistics/?action=counts`
    if (region) url += `&region=${region.id}`
    else if (country) url += `&country=${country.id}`
    const ret = await fetch(url)
    if (ret.ok) counts = await ret.json()

    let dealsUrl = `/api/case_statistics/?action=deals`
    const dealsRet = await fetch(dealsUrl)
    if (dealsRet.ok) simpleDeals = (await dealsRet.json()).deals

    let investorsUrl = `/api/case_statistics/?action=investors`
    const investorsRet = await fetch(investorsUrl)
    if (investorsRet.ok) simpleInvestors = (await investorsRet.json()).investors

    loading.set(false)
  }

  onMount(() => {
    getCounts(selRegion, selCountry)
  })

  $: filteredDeals = selRegion
    ? simpleDeals.filter(d => d.country__region_id === selRegion?.id)
    : selCountry
    ? simpleDeals.filter(d => d.country.id === selCountry?.id)
    : simpleDeals

  $: filteredInvestors = selRegion
    ? simpleInvestors.filter(inv => inv.country__region_id === selRegion?.id)
    : selCountry
    ? simpleInvestors.filter(inv => inv.country.id === selCountry?.id)
    : simpleInvestors
</script>

<svelte:head>
  <title>{$_("Case statistics")} | {$_("Land Matrix")}</title>
</svelte:head>

<div class="absolute z-10 w-full border-b border-orange bg-white py-2 dark:bg-gray-800">
  <h1 class="heading4 container mx-auto mb-3">{$_("Case statistics")}</h1>
  <div class="container mx-auto flex w-full gap-5">
    <div class="flex w-full items-center gap-2">
      <div>{$_("Region")}:</div>
      <div class="w-full">
        <VirtualListSelect
          bind:value={selRegion}
          items={$regions}
          label="name"
          on:input={async () => {
            if (selRegion) {
              selCountry = undefined
              await getCounts(selRegion, undefined)
            }
          }}
        />
      </div>
    </div>
    <div class="flex w-full items-center gap-2">
      <div>{$_("Country")}:</div>
      <div class="w-full">
        <VirtualListSelect
          bind:value={selCountry}
          items={$countries.filter(c => c.deals && c.deals.length > 0)}
          label="name"
          on:input={async () => {
            if (selCountry) {
              selRegion = undefined
              await getCounts(undefined, selCountry)
            }
          }}
        />
      </div>
    </div>
  </div>
</div>

<div class="container mx-auto mt-28">
  <QualityGoals {counts} />

  <div class="my-10">
    <StatisticsTable deals={filteredDeals} investors={filteredInvestors} />
  </div>

  <div class="my-10">
    <TimespanChanges region={selRegion} country={selCountry} />
  </div>
</div>
