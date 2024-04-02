<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import { page } from "$app/stores"

  import {
    getImplementationStatusChoices,
    getNatureOfDealChoices,
    intention_of_investment_choices,
  } from "$lib/choices"
  import type { Produce } from "$lib/filters"
  import { filters, isDefaultFilter, publicOnly } from "$lib/filters"
  import { countries, fieldChoices, regions, simpleInvestors } from "$lib/stores"
  import { ProduceGroup } from "$lib/types/deal"
  import { UserRole } from "$lib/types/user"
  import type { Country, Region } from "$lib/types/wagtail"

  import { showFilterBar } from "$components/Data/stores"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import CheckboxSwitch from "$components/LowLevel/CheckboxSwitch.svelte"
  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"
  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"

  import FilterBarNegotiationStatusToggle from "./FilterBarNegotiationStatusToggle.svelte"
  import FilterCollapse from "./FilterCollapse.svelte"
  import Wimpel from "./Wimpel.svelte"

  let produceChoices: Produce[]
  $: produceChoices = $fieldChoices
    ? [
        ...($fieldChoices.deal.crops.map(item => ({
          value: item["value"],
          label: item["label"],
          groupId: ProduceGroup.CROPS,
          group: $_("Crops"),
        })) ?? []),
        ...($fieldChoices.deal.animals.map(item => ({
          value: item["value"],
          label: item["label"],
          groupId: ProduceGroup.ANIMALS,
          group: $_("Animals"),
        })) ?? []),
        ...($fieldChoices.deal.minerals.map(item => ({
          value: item.value,
          label: item.label,
          groupId: ProduceGroup.MINERAL_RESOURCES,
          group: $_("Mineral resources"),
        })) ?? []),
      ]
    : []

  $: regionsWithGlobal = [{ id: undefined, name: $_("Global") }, ...$regions]

  $: dataDownloadURL = `/api/legacy_export/?subset=${
    $publicOnly ? "PUBLIC" : "ACTIVE"
  }&${$filters.toRESTFilterArray()}&format=`

  function trackDownload(format: string) {
    let name = "Global"
    if ($filters.country_id) {
      name = ($countries.find(c => c.id === $filters.country_id) as Country).name
    }
    if ($filters.region_id) {
      name = ($regions.find(r => r.id === $filters.region_id) as Region).name
    }

    if ($tracker) $tracker.trackEvent("Downloads", format, name)
  }

  const toggleDefaultFilter = (e: Event) => {
    $filters = (e.currentTarget as HTMLInputElement).checked
      ? $filters.empty().default()
      : $filters.empty()
  }

  const groupByProduce = (p: Produce) => p.groupId
</script>

<div
  class="absolute bottom-0 left-0 top-0 z-10 flex bg-white/90 text-sm shadow-inner drop-shadow-[3px_-3px_1px_rgba(0,0,0,0.3)] dark:bg-gray-700 {$showFilterBar
    ? 'w-[clamp(220px,20%,300px)]'
    : 'w-0'}"
>
  <Wimpel
    on:click={() => showFilterBar.set(!$showFilterBar)}
    showing={$showFilterBar}
  />
  <div
    class="flex h-full w-full flex-col overflow-y-auto p-1"
    class:hidden={!$showFilterBar}
    dir="rtl"
  >
    <div class="w-full self-start" dir="ltr">
      <h2 class="heading5 my-2 px-2">{$_("Filter")}</h2>
      <div class="my-2 px-2">
        <CheckboxSwitch
          checked={$isDefaultFilter}
          class="text-base"
          on:change={toggleDefaultFilter}
        >
          {$_("Default filter")}
        </CheckboxSwitch>

        {#if $page.data.user?.role >= UserRole.EDITOR}
          <CheckboxSwitch class="text-base" bind:checked={$publicOnly}>
            {$_("Public deals only")}
          </CheckboxSwitch>
        {/if}
      </div>

      <FilterCollapse
        clearable={!!$filters.region_id}
        on:clear={() => ($filters.region_id = undefined)}
        title={$_("Land Matrix region")}
      >
        {#each regionsWithGlobal as reg}
          <label class="block">
            <input
              type="radio"
              class="radio-btn"
              name="lm-region-filter"
              bind:group={$filters.region_id}
              value={reg.id}
              on:change={() => ($filters.country_id = undefined)}
            />
            {reg.name}
          </label>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        clearable={!!$filters.country_id}
        on:clear={() => ($filters.country_id = undefined)}
        title={$_("Country")}
      >
        <CountrySelect
          countries={$countries.filter(c => c.deals && c.deals.length > 0)}
          on:input={e => {
            $filters.country_id = e.detail?.id
          }}
          value={$countries.find(c => c.id === $filters.country_id)}
        />
      </FilterCollapse>

      <FilterCollapse
        clearable={!!($filters.deal_size_min || $filters.deal_size_max)}
        on:clear={() => ($filters.deal_size_min = $filters.deal_size_max = undefined)}
        title={$_("Deal size")}
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
        on:clear={() => ($filters.nature_of_deal = [])}
        title={$_("Nature of the deal")}
      >
        {#each Object.entries(getNatureOfDealChoices($_)) as [isval, isname]}
          <label class="block">
            <input
              type="checkbox"
              bind:group={$filters.nature_of_deal}
              value={isval}
              class="checkbox-btn"
            />
            {isname}
          </label>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        clearable={!!($filters.investor_id || $filters.investor_country_id)}
        on:clear={() =>
          ($filters.investor_id = undefined) &&
          ($filters.investor_country_id = undefined)}
        title={$_("Investor")}
      >
        {$_("Investor name")}
        <VirtualListSelect
          items={$simpleInvestors}
          label="name"
          on:input={e => ($filters.investor_id = e?.detail?.id)}
          value={$simpleInvestors.find(i => i.id === $filters.investor_id)}
        >
          <svelte:fragment let:selection slot="selection">
            {selection.name} (#{selection.id})
          </svelte:fragment>
          <svelte:fragment let:item slot="item">
            #{item.id}: {item.name}
          </svelte:fragment>
        </VirtualListSelect>
        {$_("Country of registration")}
        <CountrySelect
          countries={$countries}
          on:input={e => ($filters.investor_country_id = e.detail?.id)}
          value={$countries.find(c => c.id === $filters.investor_country_id)}
        />
      </FilterCollapse>

      <FilterCollapse
        clearable={!!($filters.initiation_year_min || $filters.initiation_year_max)}
        on:clear={() =>
          ($filters.initiation_year_min = $filters.initiation_year_max = undefined)}
        title={$_("Year of initiation")}
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
        on:clear={() => ($filters.implementation_status = [])}
        title={$_("Implementation status")}
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
        {#each Object.entries(getImplementationStatusChoices($_)) as [isval, isname]}
          <label class="block">
            <input
              bind:group={$filters.implementation_status}
              class=" checkbox-btn"
              type="checkbox"
              value={isval}
            />
            {isname}
          </label>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        clearable={$filters.intention_of_investment.length > 0}
        on:clear={() => ($filters.intention_of_investment = [])}
        title={$_("Intention of investment")}
      >
        <label class="block">
          <input
            bind:group={$filters.intention_of_investment}
            class="checkbox-btn form-checkbox"
            type="checkbox"
            value="UNKNOWN"
          />
          {$_("No information")}
        </label>
        {#each Object.entries(intention_of_investment_choices) as [name, options]}
          <div class="mb-2">
            <strong>{$_(name)}</strong>
            {#each Object.entries(options) as [isval, isname]}
              <label class="block">
                <input
                  type="checkbox"
                  bind:group={$filters.intention_of_investment}
                  value={isval}
                  class="checkbox-btn form-checkbox"
                />
                {$_(isname)}
              </label>
            {/each}
          </div>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        clearable={$filters.produce ? $filters.produce.length > 0 : false}
        on:clear={() => ($filters.produce = [])}
        title={$_("Produce")}
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
        on:clear={() => ($filters.transnational = null)}
        title={$_("Scope")}
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
        on:clear={() => ($filters.forest_concession = null)}
        title={$_("Forest concession")}
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
      <slot />
      <FilterCollapse title={$_("Download")}>
        <ul>
          <li>
            <a
              data-sveltekit-reload
              href={dataDownloadURL + "xlsx"}
              on:click={() => trackDownload("xlsx")}
            >
              <DownloadIcon />
              {$_("All attributes")} (xlsx)
            </a>
          </li>
          <li>
            <a
              data-sveltekit-reload
              href={dataDownloadURL + "csv"}
              on:click={() => trackDownload("csv")}
            >
              <DownloadIcon />
              {$_("All attributes")} (csv)
            </a>
          </li>
          <li>
            <a
              data-sveltekit-reload
              href={`/api/gis_export/?type=locations&${$filters.toRESTFilterArray()}&subset=${
                $publicOnly ? "PUBLIC" : "ACTIVE"
              }`}
              on:click={() => trackDownload("locations")}
            >
              <DownloadIcon />
              {$_("Locations (as geojson)")}
            </a>
          </li>
          <li>
            <a
              data-sveltekit-reload
              href={`/api/gis_export/?type=areas&${$filters.toRESTFilterArray()}&subset=${
                $publicOnly ? "PUBLIC" : "ACTIVE"
              }`}
              on:click={() => trackDownload("areas")}
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
