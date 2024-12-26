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

  import { filters } from "$lib/filters"
  import { createLabels, fieldChoices } from "$lib/stores"
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
    open?: boolean
    disableSubmit?: boolean
    disableAdvanced?: boolean
    onsubmit?: EventHandler<SubmitEvent, HTMLFormElement>
  }

  let {
    open = $bindable(false),
    disableSubmit = false,
    disableAdvanced = false,
    onsubmit,
  }: Props = $props()

  let filterModeGroup: FilterMode = $state("custom")
  let filterModeLabel: { [key in FilterMode]: string } = $derived({
    default: $_("Default"),
    custom: $_("Custom"),
  })
</script>

<Modal bind:open dismissible>
  <h4 class="heading4">
    {$_("Filter settings")}
  </h4>

  <hr />

  <form class="mt-6 w-full text-lg" {onsubmit}>
    <div class="min-w-[33vw] self-start" dir="ltr">
      <RegionSelect
        regions={page.data.regions}
        on:input={e => {
          if (e.detail) {
            $filters.region_id = e.detail.id
            $filters.country_id = undefined
          }
        }}
        on:clear={() => ($filters.region_id = undefined)}
        value={page.data.regions.find(c => c.id === $filters.region_id)}
      />
      <CountrySelect
        countries={page.data.countries}
        on:input={e => {
          if (e.detail) {
            $filters.country_id = e.detail.id
            $filters.region_id = undefined
          }
        }}
        on:clear={() => ($filters.country_id = undefined)}
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
              clearable={$filters.intention_of_investment.length > 0}
              on:clear={() => ($filters.intention_of_investment = [])}
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
                {@const groupValues = $fieldChoices.deal.intention_of_investment.filter(
                  entry => entry.group === group,
                )}

                <div class="mb-2">
                  <strong>
                    {createLabels($fieldChoices.deal.intention_of_investment_group)[
                      group
                    ]}
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
              {#each $fieldChoices.deal.implementation_status as { value, label }}
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
