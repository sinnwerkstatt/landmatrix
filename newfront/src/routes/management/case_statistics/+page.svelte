<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"

  import { countries, loading, regions } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"
  import type { Country, Region } from "$lib/types/wagtail"

  import type { Counts } from "./case_statistics"
  import QualityGoals from "./QualityGoals.svelte"
  import StatisticsTable from "./StatisticsTable.svelte"

  let selCountry: Country | undefined
  let selRegion: Region | undefined

  let counts: Counts = {}
  let simpleDeals: Deal[] = []
  let simpleInvestors: Investor[] = []

  async function getCounts(region: Region | undefined, country: Country | undefined) {
    loading.set(true)

    let url = `${import.meta.env.VITE_BASE_URL}/api/case_statistics/?action=counts`
    if (region) url += `&region=${region.id}`
    else if (country) url += `&country=${country.id}`
    const ret = await fetch(url)
    if (ret.ok) counts = await ret.json()

    let dealsUrl = `${import.meta.env.VITE_BASE_URL}/api/case_statistics/?action=deals`
    const dealsRet = await fetch(dealsUrl)
    if (dealsRet.ok) simpleDeals = (await dealsRet.json()).deals

    let investorsUrl = `${
      import.meta.env.VITE_BASE_URL
    }/api/case_statistics/?action=investors`
    const investorsRet = await fetch(investorsUrl)
    if (investorsRet.ok) simpleInvestors = (await investorsRet.json()).investors

    loading.set(false)
  }

  onMount(() => {
    getCounts(selRegion, selCountry)
  })

  $: filteredDeals =
    selRegion || selCountry
      ? simpleDeals.filter(d =>
          selCountry
            ? d.country_id === selCountry.id
            : d.country__region_id === selRegion.id,
        )
      : simpleDeals
  $: filteredInvestors =
    selRegion || selCountry
      ? simpleInvestors.filter(inv =>
          selCountry
            ? inv.country_id === selCountry.id
            : inv.country__region_id === selRegion.id,
        )
      : simpleInvestors
</script>

<svelte:head>
  <title>{$_("Case statistics")} | {$_("Land Matrix")}</title>
</svelte:head>

<div class="container mx-auto">
  <h1>{$_("Case statistics")}</h1>

  <div class="flex w-full gap-5">
    <div class="flex w-full items-center gap-2">
      <div>{$_("Region")}:</div>
      <div class="w-full">
        <Select
          {VirtualList}
          bind:value={selRegion}
          getOptionLabel={o => `${o.name} (#${o.id})`}
          getSelectionLabel={o => `${o.name} (#${o.id})`}
          items={$regions}
          labelIdentifier="name"
          on:clear={() => getCounts(undefined, undefined)}
          on:select={() => {
            selCountry = undefined
            getCounts(selRegion, undefined)
          }}
          optionIdentifier="id"
          placeholder={$_("Region")}
          showChevron
        />
      </div>
    </div>
    <div class="flex w-full items-center gap-2">
      <div>{$_("Country")}:</div>
      <div class="w-full">
        <Select
          {VirtualList}
          bind:value={selCountry}
          items={$countries.filter(c => c.deals && c.deals.length > 0)}
          labelIdentifier="name"
          on:clear={() => getCounts(undefined, undefined)}
          on:select={() => {
            selRegion = undefined
            getCounts(undefined, selCountry)
          }}
          optionIdentifier="id"
          placeholder={$_("Country")}
          showChevron
        />
      </div>
    </div>
  </div>

  <QualityGoals {counts} />

  <div>
    <h2 class="mt-10">{$_("Indicator listings")}</h2>
    <StatisticsTable deals={filteredDeals} investors={filteredInvestors} />
  </div>
</div>
