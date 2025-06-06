<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { dealChoices } from "$lib/fieldChoices"
  import { dealsNG } from "$lib/stores"
  import { isMobile } from "$lib/stores/basics"
  import type { DealHull } from "$lib/types/data"

  import DataContainer from "$components/Data/DataContainer.svelte"
  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table, { type Column } from "$components/Table/Table.svelte"

  let columns: Column[] = $derived([
    { key: "fully_updated_at", label: $_("Last full update"), colSpan: 2 },
    { key: "id", label: $_("ID"), colSpan: 1 },
    { key: "country_id", label: $_("Target country"), colSpan: 3 },
    {
      key: "current_intention_of_investment",
      label: $_("Current intention of investment"),
      colSpan: 5,
      submodel: "selected_version",
    },
    {
      key: "current_negotiation_status",
      label: $_("Current negotiation status"),
      colSpan: 4,
      choices: $dealChoices.negotiation_status,
      submodel: "selected_version",
    },
    {
      key: "current_implementation_status",
      label: $_("Current implementation status"),
      colSpan: 4,
      choices: $dealChoices.implementation_status,
      submodel: "selected_version",
    },
    {
      key: "current_contract_size",
      label: $_("Current contract size"),
      colSpan: 3,
      unit: $_("ha"),
      submodel: "selected_version",
    },
    {
      key: "intended_size",
      label: $_("Intended size"),
      colSpan: 3,
      unit: $_("ha"),
      submodel: "selected_version",
    },
    {
      key: "deal_size",
      label: $_("Deal size"),
      colSpan: 2,
      unit: $_("ha"),
      submodel: "selected_version",
    },
    {
      key: "operating_company",
      label: $_("Operating company"),
      colSpan: 4,
      submodel: "selected_version",
    },
  ])

  let activeColumns: string[] = $state([
    "fully_updated_at",
    "id",
    "country_id",
    "current_intention_of_investment",
    "current_negotiation_status",
    "current_implementation_status",
    "deal_size",
    "operating_company",
  ])

  onMount(() => {
    showContextBar.set(false)
    showFilterBar.set(!$isMobile)
  })

  const wrapperClass = "p-1"
  const valueClass = ""

  type fieldType = {
    fieldName: string
    obj: DealHull
  }
</script>

<svelte:head>
  <title>{$_("Deals")} | {$_("Land Matrix")}</title>
</svelte:head>

<DataContainer>
  <div class="flex h-full">
    <div
      class="h-full min-h-[3px] flex-none {$showFilterBar
        ? 'w-[clamp(220px,20%,400px)]'
        : 'w-0'}"
    ></div>

    <div class="flex h-full w-1 grow flex-col px-6 pb-6">
      <div class="flex h-20 items-center text-lg">
        {$dealsNG?.length ?? "—"}
        {$dealsNG?.length === 1 ? $_("Deal") : $_("Deals")}
      </div>

      <Table
        columns={columns.filter(c => activeColumns.includes(c.key))}
        items={$dealsNG}
        sortBy="-fully_updated_at"
      >
        {#snippet field({ fieldName, obj }: fieldType)}
          {@const col = columns.find(c => c.key === fieldName)}
          {#if col}
            <DisplayField
              fieldname={col.key}
              value={col.submodel ? obj[col.submodel][col.key] : obj[col.key]}
              {wrapperClass}
              {valueClass}
            />
          {/if}
        {/snippet}
      </Table>
    </div>
    <div
      class="h-full min-h-[3px] flex-none {$showContextBar
        ? 'w-[clamp(220px,20%,400px)]'
        : 'w-0'}"
    ></div>
  </div>

  {#snippet FilterBarSnippet()}
    <div>
      <h2 class="heading5 my-2 px-2">{$_("Data settings")}</h2>
      <FilterCollapse title={$_("Table columns")}>
        <div class="flex flex-col">
          {#each columns as opt}
            <label>
              <input type="checkbox" bind:group={activeColumns} value={opt.key} />
              {opt.label}
            </label>
          {/each}
        </div>
      </FilterCollapse>
    </div>
  {/snippet}
</DataContainer>
