<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { loading } from "$lib/stores/basics"
  import type { Country, Region } from "$lib/types/data"

  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"

  import type { Counts } from "./caseStatistics"
  import QualityGoals from "./QualityGoals.svelte"
  import StatisticsTable from "./StatisticsTable.svelte"
  import TimespanChanges from "./TimespanChanges.svelte"

  let selCountry: Country | undefined
  let selRegion: Region | undefined

  let counts: Counts = {}
  async function getCounts(region: Region | undefined, country: Country | undefined) {
    loading.set(true)

    let url = `/api/case_statistics/?action=counts`
    if (region) url += `&region=${region.id}`
    else if (country) url += `&country=${country.id}`
    const ret = await fetch(url)
    if (ret.ok) counts = await ret.json()

    loading.set(false)
  }

  onMount(() => getCounts(selRegion, selCountry))
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
          items={$page.data.regions}
          label="name"
          on:input={async () => {
            if (selRegion) {
              selCountry = undefined
            }
            await getCounts(selRegion, selCountry)
          }}
        />
      </div>
    </div>
    <div class="flex w-full items-center gap-2">
      <div>{$_("Country")}:</div>
      <div class="w-full">
        <VirtualListSelect
          bind:value={selCountry}
          items={$page.data.countries.filter(c => c.deals && c.deals.length > 0)}
          label="name"
          on:input={async () => {
            if (selCountry) {
              selRegion = undefined
            }
            await getCounts(selRegion, selCountry)
          }}
        />
      </div>
    </div>
  </div>
</div>

<div class="container mx-auto mt-28">
  <QualityGoals {counts} />

  <div class="my-10">
    <StatisticsTable {selCountry} {selRegion} />
  </div>

  <div class="my-10">
    <TimespanChanges country={selCountry} region={selRegion} />
  </div>
</div>
