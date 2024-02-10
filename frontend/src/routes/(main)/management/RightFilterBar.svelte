<script lang="ts">
  import cn from "classnames"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import { countries } from "$lib/stores"
  import type { DealHull, InvestorHull } from "$lib/types/newtypes"

  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"
  import UserSelect from "$components/LowLevel/UserSelect.svelte"

  import { managementFilters, modeMap, MODES } from "./state"
  import type { Mode } from "./state"

  export let showFilters = false
  export let objects: Array<DealHull | InvestorHull> = []
  export let model: "deal" | "investor" = "deal"

  const checkType = (o: DealHull | InvestorHull): o is DealHull => model === "deal"

  export let createdByUserIDs: Set<number>
  export let modifiedByUserIDs: Set<number>

  $: objectsCountryIDs = objects?.map(d =>
    checkType(d) ? d.country_id : d.selected_version.country_id,
  )
  $: relCountries = $countries.filter(c => objectsCountryIDs.includes(c.id))

  let modeItems: { value: Mode; label: string }[]
  $: modeItems = MODES.map(mode => ({ value: mode, label: $modeMap[mode] }))
</script>

<div
  class={cn(
    "h-full w-96 border-black bg-gray-50 p-3 drop-shadow-[-3px_-3px_3px_rgba(0,0,0,0.3)] transition-all dark:bg-gray-700",
    showFilters ? "visible " : "hidden",
  )}
>
  <h3 class="mt-0">{$_("Filters")}</h3>
  <div class="space-y-4">
    <div>
      <div class="mb-1 font-bold">{$_("Mode")}</div>
      <Select bind:justValue={$managementFilters.mode} items={modeItems} showChevron />
    </div>
    <div>
      <div class="mb-1 font-bold">{$_("Target country")}</div>
      <CountrySelect bind:value={$managementFilters.country} countries={relCountries} />
    </div>
    <hr />
    {#if model === "deal"}
      <div>
        <div class="mb-1 font-bold">{$_("Deal size")}</div>
        <div class="flex gap-1">
          <input
            bind:value={$managementFilters.dealSizeFrom}
            class="inpt"
            placeholder="From size"
            type="number"
          />
          <input
            bind:value={$managementFilters.dealSizeTo}
            class="inpt"
            placeholder="To size"
            type="number"
          />
        </div>
      </div>
      <hr />
    {/if}
    <div>
      <div class="font-bold">{$_("Created at")}</div>
      <div class="flex gap-1">
        <input
          bind:value={$managementFilters.createdAtFrom}
          class="inpt"
          placeholder="From date"
          type="date"
        />
        <input
          bind:value={$managementFilters.createdAtTo}
          class="inpt"
          placeholder="To date"
          type="date"
        />
      </div>
    </div>
    <div>
      <div class="font-bold">{$_("Created by")}</div>
      <UserSelect
        bind:value={$managementFilters.createdBy}
        userIDs={createdByUserIDs}
      />
    </div>
    <hr />
    <div>
      <div class="font-bold">{$_("Modified at")}</div>
      <div class="flex gap-1">
        <input
          bind:value={$managementFilters.modifiedAtFrom}
          class="inpt"
          placeholder="From date"
          type="date"
        />
        <input
          bind:value={$managementFilters.modifiedAtTo}
          class="inpt"
          placeholder="To date"
          type="date"
        />
      </div>
    </div>
    <div>
      <div class="font-bold">{$_("Modified by")}</div>
      <UserSelect
        bind:value={$managementFilters.modifiedBy}
        userIDs={modifiedByUserIDs}
      />
    </div>
    {#if model === "deal"}
      <hr />
      <div>
        <div class="font-bold">{$_("Fully updated at")}</div>
        <div class="flex gap-1">
          <input
            bind:value={$managementFilters.fullyUpdatedAtFrom}
            class="inpt"
            placeholder="From date"
            type="date"
          />
          <input
            bind:value={$managementFilters.fullyUpdatedAtTo}
            class="inpt"
            placeholder="To date"
            type="date"
          />
        </div>
      </div>
    {/if}
  </div>
</div>
