<script lang="ts">
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"

  import { page } from "$app/stores"

  import {
    getImplementationStatusChoices,
    getNatureOfDealChoices,
    intention_of_investment_choices,
  } from "$lib/choices"
  import { filters, isDefaultFilter, publicOnly } from "$lib/filters"
  import type { Produce } from "$lib/filters"
  import { countries, formfields, regions, simpleInvestors } from "$lib/stores"
  import { tracker } from "$lib/stores/tracker"
  import { ProduceGroup } from "$lib/types/deal"
  import { UserRole } from "$lib/types/user"
  import type { Country, Region } from "$lib/types/wagtail"

  import { showFilterBar } from "$components/Data/stores"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import CheckboxSwitch from "$components/LowLevel/CheckboxSwitch.svelte"
  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"
  import InvestorSelect from "$components/LowLevel/InvestorSelect.svelte"

  import FilterBarNegotiationStatusToggle from "./FilterBarNegotiationStatusToggle.svelte"
  import FilterCollapse from "./FilterCollapse.svelte"
  import Wimpel from "./Wimpel.svelte"

  let produceChoices: Produce[]
  $: produceChoices = $formfields
    ? [
        ...($formfields.deal.crops.choices?.map(item => ({
          value: item["value"],
          label: item["label"],
          groupId: ProduceGroup.CROPS,
          group: $_("Crops"),
        })) ?? []),
        ...($formfields.deal.animals.choices?.map(item => ({
          value: item["value"],
          label: item["label"],
          groupId: ProduceGroup.ANIMALS,
          group: $_("Animals"),
        })) ?? []),
        ...($formfields.deal.mineral_resources.choices?.map(item => ({
          value: item["value"],
          label: item["label"],
          groupId: ProduceGroup.MINERAL_RESOURCES,
          group: $_("Mineral resources"),
        })) ?? []),
      ]
    : []

  $: regionsWithGlobal = [{ id: undefined, name: $_("Global") }, ...$regions]

  $: jsonFilters = JSON.stringify($filters.toGQLFilterArray())
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

    if ($tracker) {
      $tracker.trackEvent("Downloads", format, name)
    }
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
    showing={$showFilterBar}
    on:click={() => showFilterBar.set(!$showFilterBar)}
  />
  <div
    dir="rtl"
    class="flex h-full w-full flex-col overflow-y-auto"
    class:hidden={!$showFilterBar}
  >
    <div dir="ltr" class="w-full self-start">
      <h2 class="heading5 my-2 px-2">{$_("Filter")}</h2>
      <div class="my-2 px-2">
        <CheckboxSwitch
          class="text-base"
          checked={$isDefaultFilter}
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
        title={$_("Land Matrix region")}
        clearable={!!$filters.region_id}
        on:clear={() => ($filters.region_id = undefined)}
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
        title={$_("Country")}
        clearable={!!$filters.country_id}
        on:clear={() => ($filters.country_id = undefined)}
      >
        <CountrySelect
          value={$countries.find(c => c.id === $filters.country_id)}
          countries={$countries.filter(c => c.deals && c.deals.length > 0)}
          on:input={e => {
            $filters.country_id = e.detail?.id
          }}
        />
      </FilterCollapse>

      <FilterCollapse
        title={$_("Deal size")}
        clearable={!!($filters.deal_size_min || $filters.deal_size_max)}
        on:clear={() => ($filters.deal_size_min = $filters.deal_size_max = undefined)}
      >
        <div class="field-has-appendix">
          <input
            bind:value={$filters.deal_size_min}
            type="number"
            class="inpt"
            placeholder={$_("from")}
            aria-label="from"
            max={$filters.deal_size_max}
          />
          <span>ha</span>
        </div>
        <div class="field-has-appendix">
          <input
            bind:value={$filters.deal_size_max}
            type="number"
            class="inpt"
            placeholder={$_("to")}
            aria-label="to"
            min={$filters.deal_size_min}
          />
          <span>ha</span>
        </div>
      </FilterCollapse>

      <FilterBarNegotiationStatusToggle />

      <FilterCollapse
        title={$_("Nature of the deal")}
        clearable={$filters.nature_of_deal.length > 0}
        on:clear={() => ($filters.nature_of_deal = [])}
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
        title={$_("Investor")}
        clearable={!!($filters.investor || $filters.investor_country_id)}
        on:clear={() =>
          ($filters.investor = undefined) && ($filters.investor_country_id = undefined)}
      >
        {$_("Investor name")}
        <InvestorSelect
          value={$filters.investor}
          investors={$simpleInvestors}
          on:input={e => ($filters.investor = e.detail)}
        />
        {$_("Country of registration")}
        <CountrySelect
          value={$countries.find(c => c.id === $filters.investor_country_id)}
          countries={$countries}
          on:input={e => ($filters.investor_country_id = e.detail?.id)}
        />
      </FilterCollapse>

      <FilterCollapse
        title={$_("Year of initiation")}
        clearable={!!($filters.initiation_year_min || $filters.initiation_year_max)}
        on:clear={() =>
          ($filters.initiation_year_min = $filters.initiation_year_max = undefined)}
      >
        <div class="flex gap-1">
          <input
            bind:value={$filters.initiation_year_min}
            type="number"
            class="inpt"
            placeholder="from"
            aria-label="from"
            min="1970"
            max={new Date().getFullYear()}
          />
          <input
            bind:value={$filters.initiation_year_max}
            type="number"
            class="inpt"
            placeholder="to"
            aria-label="to"
            min="1970"
            max={new Date().getFullYear()}
          />
        </div>

        <label class="block">
          <input
            id="initiation_year_unknown"
            bind:checked={$filters.initiation_year_unknown}
            type="checkbox"
            disabled={!$filters.initiation_year_min && !$filters.initiation_year_max}
          />

          {$_("Include unknown years")}
        </label>
      </FilterCollapse>

      <FilterCollapse
        title={$_("Implementation status")}
        clearable={$filters.implementation_status.length > 0}
        on:clear={() => ($filters.implementation_status = [])}
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
        title={$_("Intention of investment")}
        clearable={$filters.intention_of_investment.length > 0}
        on:clear={() => ($filters.intention_of_investment = [])}
      >
        <label class="block">
          <input
            type="checkbox"
            bind:group={$filters.intention_of_investment}
            value="UNKNOWN"
            class="checkbox-btn form-checkbox"
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
        title={$_("Produce")}
        clearable={$filters.produce ? $filters.produce.length > 0 : false}
        on:clear={() => ($filters.produce = [])}
      >
        <Select
          bind:value={$filters.produce}
          items={produceChoices}
          multiple
          showChevron
          groupBy={groupByProduce}
        />
      </FilterCollapse>

      <FilterCollapse
        title={$_("Scope")}
        clearable={$filters.transnational !== null}
        on:clear={() => ($filters.transnational = null)}
      >
        <label class="block">
          <input
            type="radio"
            name="scope-filter"
            bind:group={$filters.transnational}
            value={true}
            class="radio-btn"
          />
          {$_("Transnational")}
        </label>
        <label class="block">
          <input
            type="radio"
            name="scope-filter"
            bind:group={$filters.transnational}
            value={false}
            class="radio-btn"
          />
          {$_("Domestic")}
        </label>
      </FilterCollapse>

      <FilterCollapse
        title={$_("Forest concession")}
        clearable={$filters.forest_concession !== null}
        on:clear={() => ($filters.forest_concession = null)}
      >
        <label class="block">
          <input
            type="radio"
            name="forest-concession-filter"
            bind:group={$filters.forest_concession}
            value={null}
            class="radio-btn"
          />
          {$_("Included")}
        </label>
        <label class="block">
          <input
            type="radio"
            name="forest-concession-filter"
            bind:group={$filters.forest_concession}
            value={false}
            class="radio-btn"
          />
          {$_("Excluded")}
        </label>
        <label class="block">
          <input
            type="radio"
            name="forest-concession-filter"
            bind:group={$filters.forest_concession}
            value={true}
            class="radio-btn"
          />
          {$_("Only")}
        </label>
      </FilterCollapse>
    </div>
    <div dir="ltr" class="mt-auto w-full self-end">
      <slot />
      <FilterCollapse title={$_("Download")}>
        <ul>
          <li>
            <a
              href={dataDownloadURL + "xlsx"}
              on:click={() => trackDownload("xlsx")}
              data-sveltekit-reload
            >
              <DownloadIcon />
              {$_("All attributes")} (xlsx)
            </a>
          </li>
          <li>
            <a
              href={dataDownloadURL + "csv"}
              on:click={() => trackDownload("csv")}
              data-sveltekit-reload
            >
              <i class="fas fa-file-download" />
              <DownloadIcon />
              {$_("All attributes")} (csv)
            </a>
          </li>
          <li>
            <a
              href={`/api/gis_export/?type=locations&filters=${jsonFilters}&subset=${
                $publicOnly ? "PUBLIC" : "ACTIVE"
              }`}
              on:click={() => trackDownload("locations")}
              data-sveltekit-reload
            >
              <i class="fas fa-file-download" />
              <DownloadIcon />
              {$_("Locations (as geojson)")}
            </a>
          </li>
          <li>
            <a
              href={`/api/gis_export/?type=areas&filters=${jsonFilters}&subset=${
                $publicOnly ? "PUBLIC" : "ACTIVE"
              }`}
              on:click={() => trackDownload("areas")}
              data-sveltekit-reload
            >
              <i class="fas fa-file-download" />
              <DownloadIcon />
              {$_("Areas (as geojson)")}
            </a>
          </li>
        </ul>
      </FilterCollapse>
    </div>
  </div>
</div>
