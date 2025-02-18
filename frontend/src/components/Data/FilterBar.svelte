<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import type { Snippet } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import { twMerge } from "tailwind-merge"

  import { page } from "$app/state"

  import { createLabels, dealChoices } from "$lib/fieldChoices"
  import {
    filters,
    isDefaultFilter,
    publicOnly,
    type ProduceFilter,
  } from "$lib/filters"
  import { simpleInvestors } from "$lib/stores"
  import { IntentionOfInvestmentGroup, ProduceGroup } from "$lib/types/data"
  import { isEditorOrAbove } from "$lib/utils/permissions"

  import ContextHelper from "$components/ContextHelper.svelte"
  import { showFilterBar } from "$components/Data/stores"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import CheckboxSwitch from "$components/LowLevel/CheckboxSwitch.svelte"
  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"
  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"

  import FilterBarNegotiationStatusToggle from "./FilterBarNegotiationStatusToggle.svelte"
  import FilterCollapse from "./FilterCollapse.svelte"
  import Wimpel from "./Wimpel.svelte"

  interface Props {
    children?: Snippet
  }

  let { children }: Props = $props()

  let produceGroupLabels = $derived(
    createLabels<ProduceGroup>($dealChoices.produce_group),
  )

  let produceChoices: ProduceFilter[] = $derived([
    ...($dealChoices.crops.map(({ value, label }) => ({
      value,
      label,
      groupId: ProduceGroup.CROPS,
      group: produceGroupLabels[ProduceGroup.CROPS],
    })) ?? []),
    ...($dealChoices.animals.map(({ value, label }) => ({
      value,
      label,
      groupId: ProduceGroup.ANIMALS,
      group: produceGroupLabels[ProduceGroup.ANIMALS],
    })) ?? []),
    ...($dealChoices.minerals.map(({ value, label }) => ({
      value,
      label,
      groupId: ProduceGroup.MINERAL_RESOURCES,
      group: produceGroupLabels[ProduceGroup.MINERAL_RESOURCES],
    })) ?? []),
  ])

  let regionsWithGlobal = $derived([
    { id: undefined, name: $_("Global") },
    ...page.data.regions,
  ])

  let dataDownloadURL = $derived(
    `/api/legacy_export/?subset=${
      $publicOnly ? "PUBLIC" : "ACTIVE"
    }&${$filters.toRESTFilterArray()}&format=`,
  )

  function trackDownload(format: string) {
    let name = "Global"
    if ($filters.country_id) {
      name = page.data.countries.find(c => c.id === $filters.country_id)!.name
    }
    if ($filters.region_id) {
      name = page.data.regions.find(r => r.id === $filters.region_id)!.name
    }

    if ($tracker) $tracker.trackEvent("Downloads", format, name)
  }

  const toggleDefaultFilter = (e: Event) => {
    $filters = (e.currentTarget as HTMLInputElement).checked
      ? $filters.empty().default()
      : $filters.empty()
  }

  const groupByProduce = (p: ProduceFilter) => p.groupId
</script>

<div
  class={twMerge(
    "absolute bottom-0 left-0 top-0 z-10 flex bg-white/90 text-sm shadow-inner drop-shadow-[3px_-3px_1px_rgba(0,0,0,0.3)] dark:bg-gray-700",
    $showFilterBar ? "w-[clamp(220px,20%,400px)]" : "w-0",
  )}
>
  <Wimpel onclick={() => showFilterBar.set(!$showFilterBar)} showing={$showFilterBar} />
  <div
    class="flex h-full w-full flex-col overflow-y-auto p-1"
    class:hidden={!$showFilterBar}
    dir="rtl"
  >
    <div class="w-full self-start" dir="ltr">
      <h2 class="heading5 my-2 flex items-center gap-2 px-2">
        {$_("Filter")}
        <ContextHelper identifier="filterbar_filter" class="mb-2 size-4" />
      </h2>
      <!--      <p>{$dealsNG.length}</p>-->
      <div class="my-2 px-2">
        <CheckboxSwitch
          class="text-base"
          id="default"
          checked={$isDefaultFilter}
          onchange={toggleDefaultFilter}
        >
          {$_("Default filter")}
        </CheckboxSwitch>

        {#if isEditorOrAbove(page.data.user)}
          <CheckboxSwitch class="text-base" id="public" bind:checked={$publicOnly}>
            {$_("Public deals only")}
          </CheckboxSwitch>
        {/if}
      </div>

      <FilterCollapse
        clearable={!!$filters.region_id}
        onclear={() => ($filters.region_id = undefined)}
        title={$_("Land Matrix region")}
        contextHelp="filterbar_region"
      >
        {#each regionsWithGlobal as reg}
          <label class="block">
            <input
              type="radio"
              class="radio-btn"
              name="lm-region-filter"
              bind:group={$filters.region_id}
              value={reg.id}
              onchange={() => ($filters.country_id = undefined)}
            />
            {reg.name}
          </label>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        clearable={!!$filters.country_id}
        onclear={() => ($filters.country_id = undefined)}
        title={$_("Country")}
        contextHelp="filterbar_country"
      >
        <CountrySelect
          countries={page.data.countries.filter(c => c.deals && c.deals.length > 0)}
          oninput={e => {
            if (e.detail) {
              $filters.country_id = e.detail.id
              $filters.region_id = undefined
            }
          }}
          onclear={() => ($filters.country_id = undefined)}
          value={page.data.countries.find(c => c.id === $filters.country_id)}
        />
      </FilterCollapse>

      <FilterCollapse
        clearable={!!($filters.deal_size_min || $filters.deal_size_max)}
        onclear={() => ($filters.deal_size_min = $filters.deal_size_max = undefined)}
        title={$_("Deal size")}
        contextHelp="filterbar_dealsize"
      >
        <div class="field-has-appendix">
          <input
            aria-label="from"
            bind:value={$filters.deal_size_min}
            class="inpt"
            max={$filters.deal_size_max}
            placeholder={$_("from")}
            type="number"
          />
          <span>ha</span>
        </div>
        <div class="field-has-appendix">
          <input
            aria-label="to"
            bind:value={$filters.deal_size_max}
            class="inpt"
            min={$filters.deal_size_min}
            placeholder={$_("to")}
            type="number"
          />
          <span>ha</span>
        </div>
      </FilterCollapse>

      <FilterBarNegotiationStatusToggle />

      <FilterCollapse
        clearable={$filters.nature_of_deal.length > 0}
        onclear={() => ($filters.nature_of_deal = [])}
        title={$_("Nature of the deal")}
        contextHelp="filterbar_nature_of_deal"
      >
        {#each $dealChoices.nature_of_deal as { value, label }}
          <label class="block">
            <input
              type="checkbox"
              bind:group={$filters.nature_of_deal}
              {value}
              class="checkbox-btn"
            />
            {label}
          </label>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        clearable={!!($filters.investor_id || $filters.investor_country_id)}
        onclear={() => {
          $filters.investor_id = undefined
          $filters.investor_country_id = undefined
        }}
        title={$_("Investor")}
        contextHelp="filterbar_investor"
      >
        {$_("Investor name")}
        <VirtualListSelect
          items={$simpleInvestors.filter(i => !i.deleted && i.active)}
          label="name"
          oninput={e => ($filters.investor_id = e?.detail?.id)}
          value={$simpleInvestors.find(i => i.id === $filters.investor_id)}
        >
          {#snippet selectionSlot(selection)}
            {selection.name} (#{selection.id})
          {/snippet}
          {#snippet itemSlot(item)}
            #{item.id}: {item.name}
          {/snippet}
        </VirtualListSelect>
        {$_("Country of registration")}
        <CountrySelect
          countries={page.data.countries}
          on:input={e => ($filters.investor_country_id = e.detail?.id)}
          value={page.data.countries.find(c => c.id === $filters.investor_country_id)}
        />
      </FilterCollapse>

      <FilterCollapse
        clearable={!!($filters.initiation_year_min || $filters.initiation_year_max)}
        onclear={() =>
          ($filters.initiation_year_min = $filters.initiation_year_max = undefined)}
        title={$_("Year of initiation")}
        contextHelp="filterbar_initiation_year"
      >
        <div class="flex gap-1">
          <input
            aria-label="from"
            bind:value={$filters.initiation_year_min}
            class="inpt"
            max={new Date().getFullYear()}
            min="1970"
            placeholder="from"
            type="number"
          />
          <input
            aria-label="to"
            bind:value={$filters.initiation_year_max}
            class="inpt"
            max={new Date().getFullYear()}
            min="1970"
            placeholder="to"
            type="number"
          />
        </div>

        <label class="block">
          <input
            bind:checked={$filters.initiation_year_unknown}
            disabled={!$filters.initiation_year_min && !$filters.initiation_year_max}
            id="initiation_year_unknown"
            type="checkbox"
          />

          {$_("Include unknown years")}
        </label>
      </FilterCollapse>

      <FilterCollapse
        clearable={$filters.implementation_status.length > 0}
        onclear={() => ($filters.implementation_status = [])}
        title={$_("Implementation status")}
        contextHelp="filterbar_implementation_status"
      >
        <label class="block">
          <input
            bind:group={$filters.implementation_status}
            class="checkbox-btn"
            type="checkbox"
            value="UNKNOWN"
          />
          {$_("No information")}
        </label>
        {#each $dealChoices.implementation_status as { value, label }}
          <label class="block">
            <input
              bind:group={$filters.implementation_status}
              class=" checkbox-btn"
              type="checkbox"
              {value}
            />
            {label}
          </label>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        clearable={$filters.intention_of_investment.length > 0}
        onclear={() => ($filters.intention_of_investment = [])}
        title={$_("Intention of investment")}
        contextHelp="filterbar_intention_of_investment"
      >
        <label class="mb-2 block">
          <input
            bind:group={$filters.intention_of_investment}
            class="checkbox-btn form-checkbox"
            type="checkbox"
            value="UNKNOWN"
          />
          {$_("No information")}
        </label>
        {#each Object.keys(IntentionOfInvestmentGroup) as group}
          {@const groupValues = $dealChoices.intention_of_investment.filter(
            entry => entry.group === group,
          )}

          <div class="mb-2">
            <strong>
              {createLabels($dealChoices.intention_of_investment_group)[group]}
            </strong>

            {#each groupValues as { value, label }}
              <label class="block">
                <input
                  type="checkbox"
                  bind:group={$filters.intention_of_investment}
                  {value}
                  class="checkbox-btn form-checkbox"
                />
                {label}
              </label>
            {/each}
          </div>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        clearable={$filters.produce ? $filters.produce.length > 0 : false}
        onclear={() => ($filters.produce = [])}
        title={$_("Produce")}
        contextHelp="filterbar_produce"
      >
        <Select
          bind:value={$filters.produce}
          groupBy={groupByProduce}
          items={produceChoices}
          multiple
          showChevron
        />
      </FilterCollapse>

      <FilterCollapse
        clearable={$filters.transnational !== null}
        onclear={() => ($filters.transnational = null)}
        title={$_("Scope")}
        contextHelp="filterbar_scope"
      >
        <label class="block">
          <input
            bind:group={$filters.transnational}
            class="radio-btn"
            name="scope-filter"
            type="radio"
            value={true}
          />
          {$_("Transnational")}
        </label>
        <label class="block">
          <input
            bind:group={$filters.transnational}
            class="radio-btn"
            name="scope-filter"
            type="radio"
            value={false}
          />
          {$_("Domestic")}
        </label>
      </FilterCollapse>

      <FilterCollapse
        clearable={$filters.forest_concession !== null}
        onclear={() => ($filters.forest_concession = null)}
        title={$_("Forest concession")}
        contextHelp="filterbar_forest_concession"
      >
        <label class="block">
          <input
            bind:group={$filters.forest_concession}
            class="radio-btn"
            name="forest-concession-filter"
            type="radio"
            value={null}
          />
          {$_("Included")}
        </label>
        <label class="block">
          <input
            bind:group={$filters.forest_concession}
            class="radio-btn"
            name="forest-concession-filter"
            type="radio"
            value={false}
          />
          {$_("Excluded")}
        </label>
        <label class="block">
          <input
            bind:group={$filters.forest_concession}
            class="radio-btn"
            name="forest-concession-filter"
            type="radio"
            value={true}
          />
          {$_("Only")}
        </label>
      </FilterCollapse>
    </div>
    <div class="mt-auto w-full self-end" dir="ltr">
      {@render children?.()}
      <FilterCollapse title={$_("Download")}>
        <ul>
          <li>
            <a
              data-sveltekit-reload
              href={dataDownloadURL + "xlsx"}
              onclick={() => trackDownload("xlsx")}
            >
              <DownloadIcon />
              {$_("All attributes")} (xlsx)
            </a>
          </li>
          <li>
            <a
              data-sveltekit-reload
              href={dataDownloadURL + "csv"}
              onclick={() => trackDownload("csv")}
            >
              <DownloadIcon />
              {$_("All attributes")} (csv)
            </a>
          </li>
          <li>
            <a
              data-sveltekit-reload
              href={`/api/gis_export/locations/?${$filters.toRESTFilterArray()}&subset=${
                $publicOnly ? "PUBLIC" : "ACTIVE"
              }&format=json`}
              onclick={() => trackDownload("locations")}
            >
              <DownloadIcon />
              {$_("Locations (as geojson)")}
            </a>
          </li>
          <li>
            <a
              data-sveltekit-reload
              href={`/api/gis_export/areas/?${$filters.toRESTFilterArray()}&subset=${
                $publicOnly ? "PUBLIC" : "ACTIVE"
              }&format=json`}
              onclick={() => trackDownload("areas")}
            >
              <DownloadIcon />
              {$_("Areas (as geojson)")}
            </a>
          </li>
        </ul>
      </FilterCollapse>
    </div>
  </div>
</div>
