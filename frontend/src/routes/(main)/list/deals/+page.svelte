<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { dealsNG, fieldChoices, isMobile } from "$lib/stores"

  import DataContainer from "$components/Data/DataContainer.svelte"
  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table from "$components/Table/Table.svelte"

  let COLUMNS: {
    key: string
    label: string
    colSpan: number
  }[]
  $: COLUMNS = [
    { key: "fully_updated_at", label: $_("Last full update"), colSpan: 2 },
    { key: "id", label: $_("ID"), colSpan: 1 },
    { key: "country_id", label: $_("Target country"), colSpan: 3 },
    {
      key: "current_intention_of_investment",
      label: $_("Current intention of investment"),
      colSpan: 5,
    },
    {
      key: "current_negotiation_status",
      label: $_("Current negotiation status"),
      colSpan: 4,
      choices: $fieldChoices.deal.negotiation_status,
    },
    {
      key: "current_implementation_status",
      label: $_("Current implementation status"),
      colSpan: 4,
      choices: $fieldChoices.deal.implementation_status,
    },
    {
      key: "current_contract_size",
      label: $_("Current contract size"),
      colSpan: 3,
      unit: $_("ha"),
    },
    { key: "intended_size", label: $_("Intended size"), colSpan: 3, unit: $_("ha") },
    { key: "deal_size", label: $_("Deal size"), colSpan: 2, unit: $_("ha") },
    {
      key: "operating_company",
      label: $_("Operating company"),
      colSpan: 4,
    },
  ]

  let activeColumns: string[] = [
    "fully_updated_at",
    "id",
    "country_id",
    "current_intention_of_investment",
    "current_negotiation_status",
    "current_implementation_status",
    "deal_size",
    "operating_company",
  ]

  let labels: string[]
  $: labels = COLUMNS.filter(c => activeColumns.includes(c.key)).map(c => c.label)
  let spans: number[]
  $: spans = COLUMNS.filter(c => activeColumns.includes(c.key)).map(c => c.colSpan)

  onMount(() => {
    showContextBar.set(false)
    showFilterBar.set(!$isMobile)
  })

  const wrapperClass = "p-1"
  const valueClass = ""
</script>

<DataContainer>
  <div class="flex h-full">
    <div
      class="h-full min-h-[3px] flex-none {$showFilterBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />

    <div class="flex h-full w-1 grow flex-col px-6 pb-6">
      <div class="flex h-20 items-center text-lg">
        {$dealsNG?.length ?? "—"}
        {$dealsNG?.length === 1 ? $_("Deal") : $_("Deals")}
      </div>

      <Table
        columns={activeColumns}
        items={$dealsNG}
        {labels}
        sortBy="-fully_updated_at"
        {spans}
      >
        <svelte:fragment let:fieldName let:obj slot="field">
          {@const col = COLUMNS.find(c => c.key === fieldName)}
          {#if col}
            {#if ["operating_company", "current_intention_of_investment", "current_contract_size", "intended_size", "deal_size"].includes(fieldName)}
              <DisplayField
                fieldname={fieldName}
                value={obj.selected_version[fieldName]}
                {wrapperClass}
                {valueClass}
              />
            {:else}
              <DisplayField
                fieldname={fieldName}
                value={obj[fieldName]}
                {wrapperClass}
                {valueClass}
              />
            {/if}
          {/if}
        </svelte:fragment>
      </Table>
    </div>
    <div
      class="h-full min-h-[3px] flex-none {$showContextBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />
  </div>

  <div slot="FilterBar">
    <h2 class="heading5 my-2 px-2">{$_("Data settings")}</h2>
    <FilterCollapse title={$_("Table columns")}>
      <div class="flex flex-col">
        {#each COLUMNS as opt}
          <label>
            <input type="checkbox" bind:group={activeColumns} value={opt.key} />
            {opt.label}
          </label>
        {/each}
      </div>
    </FilterCollapse>
  </div>
</DataContainer>
