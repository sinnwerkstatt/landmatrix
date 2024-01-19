<script lang="ts">
  import { _ } from "svelte-i18n"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table from "$components/Table/Table.svelte"

  import type { CaseStatisticsDeal, CaseStatisticsInvestor } from "./caseStatistics"

  export let objects: Array<CaseStatisticsDeal | CaseStatisticsInvestor> = []
  export let model: "deal" | "investor" = "deal"

  interface Col {
    key: string
    label: string
    colSpan: number
  }

  const dealColumns: Col[] = [
    { key: "id", label: $_("ID"), colSpan: 1 },
    { key: "mode", label: $_("Mode"), colSpan: 2 },
    { key: "country_id", label: $_("Target country"), colSpan: 2 },
    { key: "deal_size", label: $_("Deal size"), colSpan: 2 },
    { key: "confidential", label: $_("Confidential"), colSpan: 2 },
    { key: "created_at", label: $_("Created at"), colSpan: 2 },
    { key: "modified_at", label: $_("Last update"), colSpan: 2 },
    { key: "fully_updated_at", label: $_("Last full update"), colSpan: 3 },
  ]
  const investorColumns: Col[] = [
    { key: "id", label: $_("ID"), colSpan: 1 },
    { key: "mode", label: $_("Mode"), colSpan: 2 },
    { key: "name", label: $_("Name"), colSpan: 5 },
    { key: "country_id", label: $_("Country of registration/origin"), colSpan: 4 },

    { key: "created_at", label: $_("Created at"), colSpan: 2 },
    { key: "modified_at", label: $_("Last update"), colSpan: 2 },
  ]

  let relColumns: Col[]
  $: relColumns = model === "deal" ? dealColumns : investorColumns
  $: columns = relColumns.map(x => x.key)
  $: labels = relColumns.map(x => x.label)
  $: spans = relColumns.map(x => x.colSpan)

  const wrapperClass = ""
  const valueClass = "text-gray-700 dark:text-white"
</script>

<Table {columns} items={objects} {labels} rowHeightInPx={36} {spans}>
  <svelte:fragment let:fieldName let:obj slot="field">
    {#if fieldName === "id"}
      <DisplayField fieldname="id" value={obj.id} {wrapperClass} {valueClass} {model} />
    {:else if fieldName === "mode"}
      <div class="whitespace-nowrap">{obj.mode}</div>
    {:else if fieldName === "name"}
      <DisplayField
        fieldname="name"
        model="investor"
        value={obj.active_version__name}
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "country_id"}
      <DisplayField
        fieldname="country"
        value={obj.country_id}
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "deal_size"}
      <DisplayField
        fieldname={fieldName}
        value={obj.active_version__deal_size}
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "confidential"}
      <DisplayField
        value={obj.confidential}
        fieldname={fieldName}
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "created_at"}
      <DisplayField
        value={obj.created_at}
        fieldname="created_at"
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "modified_at"}
      <DisplayField
        value={obj.modified_at}
        fieldname="modified_at"
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "fully_updated_at"}
      <DisplayField
        value={obj.fully_updated_at}
        fieldname="fully_updated_at"
        {wrapperClass}
        {valueClass}
      />
    {:else}
      {fieldName}
    {/if}
  </svelte:fragment>
</Table>
