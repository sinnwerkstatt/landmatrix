<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"

  import { countries, loading, regions } from "$lib/stores"
  import type { Country, Region } from "$lib/types/wagtail"

  let selCountry: Country | undefined
  let selRegion: Region | undefined

  type Counts = {
    deals_public_count?: number
    deals_public_multi_ds_count?: number
    deals_public_high_geo_accuracy?: number
    deals_public_polygons?: number
  }

  let counts: Counts = {}
  async function getCounts(region: Region | undefined, country: Country | undefined) {
    loading.set(true)

    let url = `${import.meta.env.VITE_BASE_URL}/api/case_statistics/?action=counts`
    if (region) url += `&region=${region.id}`
    else if (country) url += `&country=${country.id}`
    const ret = await fetch(url)
    if (ret.ok) counts = await ret.json()

    loading.set(false)
  }

  onMount(() => {
    getCounts(selRegion, selCountry)
  })

  console.log("huhu")
  function getRatio(n: number) {
    if (!counts.deals_public_count) return " "
    return ((n / counts.deals_public_count ?? 1) * 100).toFixed(1) + " %"
  }
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
          items={$regions}
          bind:value={selRegion}
          placeholder={$_("Region")}
          on:select={() => {
            selCountry = undefined
            getCounts(selRegion, undefined)
          }}
          on:clear={() => getCounts(undefined, undefined)}
          optionIdentifier="id"
          labelIdentifier="name"
          getOptionLabel={o => `${o.name} (#${o.id})`}
          getSelectionLabel={o => `${o.name} (#${o.id})`}
          showChevron
          {VirtualList}
        />
      </div>
    </div>
    <div class="flex w-full items-center gap-2">
      <div>{$_("Country")}:</div>
      <div class="w-full">
        <Select
          items={$countries.filter(c => c.deals && c.deals.length > 0)}
          bind:value={selCountry}
          placeholder={$_("Country")}
          on:select={() => {
            selRegion = undefined
            getCounts(undefined, selCountry)
          }}
          on:clear={() => getCounts(undefined, undefined)}
          optionIdentifier="id"
          labelIdentifier="name"
          showChevron
          {VirtualList}
        />
      </div>
    </div>
  </div>

  <h2 class="mt-10">{$_("Quality goals")}</h2>
  <div
    class="my-8 flex items-center justify-evenly gap-4 bg-neutral-300 p-2 text-center"
  >
    <div class="flex flex-col items-center gap-2">
      <div class="bg-neutral-200 p-3 font-bold drop-shadow-lg">
        <div class="text-2xl">{counts.deals_public_count}</div>
        <div>&nbsp;</div>
      </div>
      <div>{$_("Publicly visible deals")}</div>
      <div class="text-[10px]">
        {$_("Active deals with public filter ok, not confidential.")}
      </div>
    </div>
    <div class="flex flex-col items-center gap-2">
      <div class="bg-neutral-200 p-3  font-bold drop-shadow-lg">
        <div class="text-2xl">{counts.deals_public_multi_ds_count}</div>
        <div>{getRatio(counts.deals_public_multi_ds_count)}</div>
      </div>
      {$_("Deals with with multiple data sources")}
      <div class="text-[10px]">&nbsp;</div>
    </div>
    <div class="flex flex-col items-center gap-2">
      <div class="bg-neutral-200 p-3 font-bold drop-shadow-lg">
        <div class="text-2xl">{counts.deals_public_high_geo_accuracy}</div>
        <div>{getRatio(counts.deals_public_high_geo_accuracy)}</div>
      </div>
      {$_("Deals georeferenced with high accuracy")}
      <div class="text-[10px]">
        {$_(
          "Deals with at least one location with either accuracy level 'Coordinates' or 'Exact location' or at least one polygon.",
        )}
      </div>
    </div>
    <div class="flex flex-col items-center gap-2">
      <div class="bg-neutral-200 p-3 font-bold drop-shadow-lg">
        <div class="text-2xl">{counts.deals_public_polygons}</div>
        <div>{getRatio(counts.deals_public_polygons)}</div>
      </div>
      {$_("Deals with polygon data")}
      <div class="text-[10px]">&nbsp;</div>
    </div>
  </div>

  <h2 class="mt-10">{$_("Indicator listings")}</h2>
  <div
    class="my-8 flex items-center justify-evenly gap-4 bg-neutral-300 p-2 text-center"
  />
</div>
