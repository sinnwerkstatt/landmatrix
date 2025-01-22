<script lang="ts">
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import { twMerge } from "tailwind-merge"

  import { page } from "$app/state"

  import { stateMap } from "$lib/newUtils"
  import { Version2Status, type DealHull, type InvestorHull } from "$lib/types/data"

  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"
  import UserSelect from "$components/LowLevel/UserSelect.svelte"

  import { managementFilters } from "./state"

  const checkType = (_o: DealHull | InvestorHull): _o is DealHull => model === "deal"

  interface Props {
    showFilters?: boolean
    objects?: Array<DealHull | InvestorHull>
    model?: "deal" | "investor"
    createdByUserIDs: Set<number>
    modifiedByUserIDs: Set<number>
  }

  let {
    showFilters = false,
    objects = [],
    model = "deal",
    createdByUserIDs,
    modifiedByUserIDs,
  }: Props = $props()

  let objectsCountryIDs = $derived(
    objects?.map(d => (checkType(d) ? d.country_id : d.selected_version.country_id)),
  )
  let relCountries = $derived(
    page.data.countries.filter(c => objectsCountryIDs.includes(c.id)),
  )

  // const STATI = Object.values(Version2Status)
  const RELEVANT_STATI = [
    Version2Status.DRAFT,
    Version2Status.REVIEW,
    Version2Status.ACTIVATION,
  ]
  let statusItems: { value: Version2Status; label: string }[] = $derived(
    Object.values(Version2Status)
      .filter(v => RELEVANT_STATI.includes(v))
      .map(v => ({
        value: v,
        label: $stateMap[v].title,
      })),
  )
</script>

<div
  class={twMerge(
    "h-full w-96 border-black bg-gray-50 p-3 drop-shadow-[-3px_-3px_3px_rgba(0,0,0,0.3)] transition-all dark:bg-gray-700",
    showFilters ? "visible " : "hidden",
  )}
>
  <h3 class="mt-0">{$_("Filters")}</h3>
  <div class="space-y-4">
    <div>
      <div class="mb-1 font-bold">{$_("Status")}</div>
      <Select
        bind:justValue={$managementFilters.status}
        items={statusItems}
        showChevron
      />
    </div>
    <div>
      <div class="mb-1 font-bold">{$_("Target country")}</div>
      <CountrySelect
        value={$managementFilters.country}
        oninput={e => ($managementFilters.country = e.detail)}
        countries={relCountries}
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
      <UserSelect
        bind:value={$managementFilters.createdByID}
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
        bind:value={$managementFilters.modifiedByID}
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
