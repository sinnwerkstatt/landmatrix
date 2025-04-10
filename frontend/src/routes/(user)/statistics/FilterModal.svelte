<script lang="ts" module>
  export const FILTER_MODES = ["custom", "default"] as const
  export type FilterMode = (typeof FILTER_MODES)[number]
</script>

<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import type { EventHandler } from "svelte/elements"
  import { slide } from "svelte/transition"

  import { page } from "$app/state"

  import { createLabels, dealChoices } from "$lib/fieldChoices"
  import { filters } from "$lib/filters"
  import { IntentionOfInvestmentGroup } from "$lib/types/data"

  import FilterBarNegotiationStatusToggle from "$components/Data/FilterBarNegotiationStatusToggle.svelte"
  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import CountrySelect from "$components/LowLevel/CountrySelect.svelte"
  import RegionSelect from "$components/LowLevel/RegionSelect.svelte"
  import Modal from "$components/Modal.svelte"

  const handleFilterModeChange = (mode: FilterMode) => {
    $filters = mode === "default" ? $filters.empty().default() : $filters.empty()
  }

  onMount(() => {
    $filters = $filters.empty()
  })

  interface Props {
    open: boolean
    disableSubmit?: boolean
    disableAdvanced?: boolean
    onsubmit?: EventHandler<SubmitEvent, HTMLFormElement>
  }

  let {
    open = $bindable(),
    disableSubmit = false,
    disableAdvanced = false,
    onsubmit,
  }: Props = $props()

  let filterModeGroup: FilterMode = $state("custom")
  let filterModeLabel: { [key in FilterMode]: string } = $derived({
    default: $_("Default"),
    custom: $_("Custom"),
  })

  const ioiGroupLabels = $derived(
    createLabels($dealChoices.intention_of_investment_group),
  )
</script>

<Modal bind:open dismissible>
  <h4 class="heading4">
    {$_("Filter settings")}
  </h4>

  <hr />

  <form class="mt-6 w-full text-lg" {onsubmit}>
    <div class="min-w-[33dvw] self-start" dir="ltr">
      <RegionSelect
        onclear={() => ($filters.region_id = undefined)}
        oninput={e => {
          if (e.detail) {
            $filters.region_id = e.detail.id
            $filters.country_id = undefined
          }
        }}
        regions={page.data.regions}
        value={page.data.regions.find(c => c.id === $filters.region_id)}
      />
      <CountrySelect
        countries={page.data.countries}
        onclear={() => ($filters.country_id = undefined)}
        oninput={e => {
          if (e.detail) {
            $filters.country_id = e.detail.id
            $filters.region_id = undefined
          }
        }}
        value={page.data.countries.find(c => c.id === $filters.country_id)}
      />

      {#if !disableAdvanced}
        <div class="my-2 mt-4 flex items-baseline gap-6">
          <span class="inline after:content-[':']">
            {$_("Filter sets")}
          </span>

          <ul class="flex gap-6">
            {#each FILTER_MODES as filterMode, index}
              {@const id = `filter-mode-input-${index}`}

              <li class="inline-flex items-baseline gap-2">
                <input
                  {id}
                  bind:group={filterModeGroup}
                  class="radio-btn"
                  name="filter-mode"
                  type="radio"
                  value={filterMode}
                  onclick={() => handleFilterModeChange(filterMode)}
                />
                <label for={id} class="block">
                  {filterModeLabel[filterMode]}
                </label>
              </li>
            {/each}
          </ul>
        </div>

        {#if filterModeGroup === "custom"}
          <div transition:slide={{ duration: 200 }}>
            <FilterCollapse
              clearable={$filters.transnational !== null}
              onclear={() => ($filters.transnational = null)}
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
              clearable={$filters.intention_of_investment.length > 0}
              onclear={() => ($filters.intention_of_investment = [])}
              title={$_("Intention of investment")}
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
                    {ioiGroupLabels[group]}
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

            <FilterBarNegotiationStatusToggle />

            <FilterCollapse
              clearable={$filters.implementation_status.length > 0}
              onclear={() => ($filters.implementation_status = [])}
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
              clearable={$filters.carbon_offset_project !== null}
              on:clear={() => ($filters.carbon_offset_project = null)}
              title={$_("Carbon offset project")}
            >
              <label class="block">
                <input
                  bind:group={$filters.carbon_offset_project}
                  class="radio-btn"
                  name="carbon-offset-project-filter"
                  type="radio"
                  value={null}
                />
                {$_("No information")}
              </label>
              <label class="block">
                <input
                  bind:group={$filters.carbon_offset_project}
                  class="radio-btn"
                  name="carbon-offset-project-filter"
                  type="radio"
                  value={true}
                />
                {$_("Yes")}
              </label>
              <label class="block">
                <input
                  bind:group={$filters.carbon_offset_project}
                  class="radio-btn"
                  name="carbon-offset-project-filter"
                  type="radio"
                  value={false}
                />
                {$_("No")}
              </label>
            </FilterCollapse>

            <FilterCollapse
              clearable={$filters.produce_info_carbon_offsetting !== null}
              on:clear={() => ($filters.produce_info_carbon_offsetting = null)}
              title={$_("Produce info: Carbon sequestration/offsetting")}
            >
              <label class="block">
                <input
                  bind:group={$filters.produce_info_carbon_offsetting}
                  class="radio-btn"
                  name="produce-info-carbon-offsetting-filter"
                  type="radio"
                  value={null}
                />
                {$_("No information")}
              </label>
              <label class="block">
                <input
                  bind:group={$filters.produce_info_carbon_offsetting}
                  class="radio-btn"
                  name="produce-info-carbon-offsetting-filter"
                  type="radio"
                  value={true}
                />
                {$_("Yes")}
              </label>
              <label class="block">
                <input
                  bind:group={$filters.produce_info_carbon_offsetting}
                  class="radio-btn"
                  name="produce-info-carbon-offsetting-filter"
                  type="radio"
                  value={false}
                />
                {$_("No")}
              </label>
            </FilterCollapse>
          </div>
        {/if}
      {:else}
        <div class="h-20"></div>
      {/if}
    </div>

    <div class="mt-14 flex justify-end gap-4">
      <button class="btn-outline" onclick={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="btn btn-violet" type="submit" disabled={disableSubmit}>
        {$_("Apply")}
      </button>
    </div>
  </form>
</Modal>
