<script lang="ts">
  import { gql } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"

  import { page } from "$app/stores"

  import {
    getImplementationStatusChoices,
    getNatureOfDealChoices,
    intention_of_investment_choices,
  } from "$lib/choices"
  import { filters, isDefaultFilter, publicOnly } from "$lib/filters"
  import { countries, formfields, regions } from "$lib/stores"
  import { ProduceGroup } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"
  import { UserRole } from "$lib/types/user"

  import { showFilterBar } from "$components/Data/stores"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import CheckboxSwitch from "$components/LowLevel/CheckboxSwitch.svelte"
  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"

  import FilterBarNegotiationStatusToggle from "./FilterBarNegotiationStatusToggle.svelte"
  import FilterCollapse from "./FilterCollapse.svelte"
  import Wimpel from "./Wimpel.svelte"

  $: user = $page.data.user

  $: produceChoices = $formfields
    ? [
        ...Object.entries($formfields.deal.crops.choices).map(([v, k]) => ({
          value: v,
          label: k,
          groupID: ProduceGroup.CROPS,
          group: $_("Crops"),
        })),
        ...Object.entries($formfields.deal.animals.choices).map(([v, k]) => ({
          value: v,
          label: k,
          groupID: ProduceGroup.ANIMALS,
          group: $_("Animals"),
        })),
        ...Object.entries($formfields.deal.mineral_resources.choices).map(([v, k]) => ({
          value: v,
          label: k,
          groupID: ProduceGroup.MINERAL_RESOURCES,
          group: $_("Mineral resources"),
        })),
      ]
    : []

  $: regionsWithGlobal = [{ id: undefined, name: $_("Global") }, ...$regions]

  let investors: Investor[] = []

  async function getInvestors() {
    const { data } = await $page.data.urqlClient
      .query<{ investors: Investor[] }>(
        gql`
          query SInvestors($subset: Subset) {
            investors(limit: 0, subset: $subset) {
              id
              name
            }
          }
        `,
        { subset: user?.is_authenticated ? "UNFILTERED" : "PUBLIC" },
      )
      .toPromise()
    investors = data.investors
  }

  onMount(() => {
    getInvestors()
  })

  $: jsonFilters = JSON.stringify($filters.toGQLFilterArray())
  $: dataDownloadURL = `/api/legacy_export/?filters=${jsonFilters}&subset=${
    $publicOnly ? "PUBLIC" : "ACTIVE"
  }&format=`

  function trackDownload(format) {
    let name = "Global"
    if ($filters.country_id)
      name = $countries.find(c => c.id === $filters.country_id).name
    if ($filters.region_id) name = $regions.find(r => r.id === $filters.region_id).name

    if (window._paq) window._paq.push(["trackEvent", "Downloads", format, name])
  }
</script>

<div
  class="absolute top-0 left-0 bottom-0 z-10 flex bg-white/80 text-sm drop-shadow-[3px_-3px_1px_rgba(0,0,0,0.3)] {$showFilterBar
    ? 'w-[clamp(220px,20%,300px)]'
    : 'w-0'}"
>
  <Wimpel
    showing={$showFilterBar}
    on:click={() => showFilterBar.set(!$showFilterBar)}
  />
  <div
    class="flex h-full w-full flex-col overflow-y-auto overflow-x-hidden p-2"
    class:hidden={!$showFilterBar}
  >
    <div class="w-full self-start">
      <h3 class="my-2 text-black">{$_("Filter")}</h3>
      <CheckboxSwitch
        class="text-base"
        checked={$isDefaultFilter}
        on:change={val =>
          val.target.checked
            ? filters.set($filters.empty().default())
            : filters.set($filters.empty())}
      >
        {$_("Default filter")}
      </CheckboxSwitch>

      {#if $page.data.user?.role >= UserRole.EDITOR}
        <CheckboxSwitch class="text-base" bind:checked={$publicOnly}>
          {$_("Public deals only")}
        </CheckboxSwitch>
      {/if}

      <FilterCollapse
        title={$_("Land Matrix region")}
        clearable={!!$filters.region_id}
        on:click={() => ($filters.region_id = undefined)}
      >
        {#each regionsWithGlobal as reg}
          <label class="block">
            <input
              type="radio"
              class="radio-btn"
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
        on:click={() => ($filters.country_id = null)}
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
        on:click={() => ($filters.deal_size_min = $filters.deal_size_max = undefined)}
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
        on:click={() => ($filters.nature_of_deal = [])}
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
        on:click={() =>
          ($filters.investor = null) && ($filters.investor_country_id = null)}
      >
        {$_("Investor name")}
        <Select
          items={investors}
          bind:value={$filters.investor}
          placeholder={$_("Investor")}
          itemId="id"
          label="name"
          getOptionLabel={o => `${o.name} (#${o.id})`}
          getSelectionLabel={o => `${o.name} (#${o.id})`}
          showChevron
          {VirtualList}
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
        on:click={() =>
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
        on:click={() => ($filters.implementation_status = [])}
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
        on:click={() => ($filters.intention_of_investment = [])}
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
        clearable={$filters.produce?.length > 0}
        on:click={() => ($filters.produce = [])}
      >
        <Select
          bind:value={$filters.produce}
          items={produceChoices}
          multiple
          showChevron
          groupBy={i => i.group}
        />
      </FilterCollapse>

      <FilterCollapse
        title={$_("Scope")}
        clearable={$filters.transnational !== null}
        on:click={() => ($filters.transnational = null)}
      >
        <label class="block">
          <input
            type="radio"
            bind:group={$filters.transnational}
            value={true}
            class="radio-btn"
          />
          {$_("Transnational")}
        </label>
        <label class="block">
          <input
            type="radio"
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
        on:click={() => ($filters.forest_concession = null)}
      >
        <label class="block">
          <input
            type="radio"
            bind:group={$filters.forest_concession}
            value={null}
            class="radio-btn"
          />
          {$_("Included")}
        </label>
        <label class="block">
          <input
            type="radio"
            bind:group={$filters.forest_concession}
            value={false}
            class="radio-btn"
          />
          {$_("Excluded")}
        </label>
        <label class="block">
          <input
            type="radio"
            bind:group={$filters.forest_concession}
            value={true}
            class="radio-btn"
          />
          {$_("Only")}
        </label>
      </FilterCollapse>
    </div>
    <div class="mt-auto w-full self-end pt-10">
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
