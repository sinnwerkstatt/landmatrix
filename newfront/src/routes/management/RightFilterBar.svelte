<script lang="ts">
  import cn from "classnames"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"

  import { allUsers, countries } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"

  import { managementFilters } from "./state"

  export let showFilters = false
  export let objects: Array<Deal | Investor> = []
  export let model: "deal" | "investor" = "deal"
  // export let possibleUsers: User[] = []

  $: objectsCountryIDs = objects?.map(d => d.country?.id)
  $: relCountries = $countries.filter(c => objectsCountryIDs.includes(c.id))
</script>

<div
  class={cn(
    "h-full w-96 border-black bg-neutral-100  p-3 drop-shadow-[-3px_-3px_3px_rgba(0,0,0,0.3)] transition-all",
    showFilters ? "visible " : "hidden",
  )}
>
  <h3 class="mt-0">{$_("Filters")}</h3>
  <div class="space-y-4">
    <div>
      <div class="mb-1 font-bold">{$_("Target country")}</div>
      <Select
        {VirtualList}
        bind:value={$managementFilters.country}
        getOptionLabel={o => `${o.name} (#${o.id})`}
        getSelectionLabel={o => `${o.name} (#${o.id})`}
        items={relCountries}
        labelIdentifier="name"
        optionIdentifier="id"
        placeholder={$_("Target country")}
        showChevron
      />
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
      <div>
        <Select
          {VirtualList}
          bind:value={$managementFilters.createdBy}
          getOptionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
          getSelectionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
          items={$allUsers}
          optionIdentifier="id"
          placeholder={$_("User")}
          showChevron
        />
      </div>
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
      <div>
        <Select
          {VirtualList}
          bind:value={$managementFilters.modifiedBy}
          getOptionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
          getSelectionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
          items={$allUsers}
          optionIdentifier="id"
          placeholder={$_("User")}
          showChevron
        />
      </div>
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
