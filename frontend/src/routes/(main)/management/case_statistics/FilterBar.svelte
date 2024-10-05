<script context="module" lang="ts">
  import { writable } from "svelte/store"

  import type { Country, Region } from "$lib/types/data"

  export interface Filters {
    country: Country | null
    region: Region | null
  }

  export const filters = writable<Filters>({ country: null, region: null })
</script>

<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { page } from "$app/stores"

  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"

  $: countries = $page.data.countries
    .filter(c => c.deals && c.deals.length > 0)
    .filter(c => ($filters.region ? c.region_id === $filters.region?.id : true))
</script>

<div class="m-2 flex flex-col gap-2">
  <!--  <button-->
  <!--    class="text-left hover:text-gray-700 dark:hover:text-gray-100"-->
  <!--    on:click={() => {-->
  <!--      showFilter = !showFilter-->
  <!--    }}-->
  <!--    title={$_("Show filter")}-->
  <!--  >-->
  <!--    <span class="inline-block transition-transform" class:rotate-180={showFilter}>-->
  <!--      <ChevronDownIcon />-->
  <!--    </span>-->
  <!--    <span class="subtitle1">-->
  <!--      {$_("Filter")}:-->
  <!--      <span class="italic">-->
  <!--        {$filters.region?.name ?? ""} &#45;&#45;-->
  <!--        {$filters.country?.name ?? ""}-->
  <!--      </span>-->
  <!--    </span>-->
  <!--  </button>-->

  <!--  {#if showFilter}-->
  <div
    class="grid w-full grid-rows-2 gap-4 lg:grid-cols-2 lg:grid-rows-1"
    transition:slide
  >
    <div class="flex items-center gap-2">
      <label for="region-filter" class="after:content-[':']">
        {$_("Region")}
      </label>
      <VirtualListSelect
        id="region-filter"
        value={$filters.region}
        items={$page.data.regions}
        label="name"
        on:input={e => {
          if (e.detail) {
            $filters.region = e.detail
            $filters.country = null
          }
        }}
        on:clear={() => {
          $filters.region = null
          $filters.country = null
        }}
      />
    </div>

    <div class="flex items-center gap-2">
      <label for="country-filter" class="after:content-[':']">
        {$_("Country")}
      </label>
      <VirtualListSelect
        id="country-filter"
        value={$filters.country}
        items={countries}
        label="name"
        on:input={e => {
          if (e.detail) {
            $filters.country = e.detail
          }
        }}
        on:clear={() => {
          $filters.country = null
        }}
      />
    </div>
  </div>
  <!--{/if}-->
</div>
