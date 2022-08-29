<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"
  import type { Writable } from "svelte/store"

  import { page } from "$app/stores"

  import { countries, getUsers } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"
  import type { User } from "$lib/types/user"

  import Overlay from "$components/Overlay.svelte"

  import { managementFilters } from "./state"

  export let visible
  export let objects: Array<Deal | Investor> = []
  export let model: "deal" | "investor" = "deal"

  let users: Writable<User[]>

  $: objectsCountryIDs = objects?.map(d => d.country?.id)
  $: relCountries = $countries.filter(c => objectsCountryIDs.includes(c.id))

  onMount(async () => {
    users = await getUsers($page.data.urqlClient)
  })
</script>

<Overlay bind:visible closeButtonText={$_("Close")} title={$_("Filters")}>
  <div class="space-y-4">
    <div class="flex items-center">
      <div class="w-3/12 font-bold">{$_("Target country")}</div>
      <div class="w-9/12">
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
    </div>
    {#if model === "deal"}
      <div class="flex items-center">
        <div class="w-3/12 font-bold">{$_("Deal size")}</div>
        <div class="flex w-9/12 gap-1">
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
    {/if}

    <div class="flex items-center">
      <div class="w-3/12 font-bold">{$_("Creation")}</div>
      <div class="flex w-9/12 gap-4">
        <div class="flex w-3/5 gap-1">
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
        <div class="w-2/5">
          <Select
            {VirtualList}
            bind:value={$managementFilters.createdBy}
            getOptionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
            getSelectionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
            items={$users}
            optionIdentifier="id"
            placeholder={$_("User")}
            showChevron
          />
        </div>
      </div>
    </div>

    <div class="flex items-center">
      <div class="w-3/12 font-bold">{$_("Modified at")}</div>
      <div class="flex w-9/12 gap-1">
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
    <div class="flex items-center">
      <div class="w-3/12 font-bold">{$_("Modified by")}</div>
      <div class="w-9/12">
        <Select
          {VirtualList}
          bind:value={$managementFilters.modifiedBy}
          getOptionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
          getSelectionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
          items={$users}
          optionIdentifier="id"
          placeholder={$_("User")}
          showChevron
        />
      </div>
    </div>
  </div>
</Overlay>
