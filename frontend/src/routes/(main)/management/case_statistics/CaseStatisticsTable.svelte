<script lang="ts">
  import { dealFields, investorFields } from "$lib/fieldLookups.js"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table from "$components/Table/Table.svelte"

  import type { CaseStatisticsDeal, CaseStatisticsInvestor } from "./caseStatistics"

  export let objects: Array<CaseStatisticsDeal | CaseStatisticsInvestor> = []
  export let model: "deal" | "investor" = "deal"
  export let linkDraftVersion: boolean

  interface Col {
    key: string
    colSpan: number
  }

  const dealColumns: Col[] = [
    { key: "id", colSpan: 1 },
    { key: "status", colSpan: 2 },
    { key: "country_id", colSpan: 2 },
    { key: "deal_size", colSpan: 2 },
    { key: "confidential", colSpan: 2 },
    { key: "created_at", colSpan: 2 },
    { key: "modified_at", colSpan: 2 },
    { key: "fully_updated_at", colSpan: 3 },
  ]
  const investorColumns: Col[] = [
    { key: "id", colSpan: 1 },
    { key: "status", colSpan: 2 },
    { key: "name", colSpan: 5 },
    { key: "country_id", colSpan: 4 },
    { key: "created_at", colSpan: 2 },
    { key: "modified_at", colSpan: 2 },
  ]

  let relColumns: Col[]
  $: relColumns = model === "deal" ? dealColumns : investorColumns
  $: columns = relColumns.map(x => x.key)
  $: labels = relColumns.map(x =>
    model === "deal" ? $dealFields[x.key].label : $investorFields[x.key].label,
  )
  $: spans = relColumns.map(x => x.colSpan)

  const wrapperClass = ""
  const valueClass = "text-gray-700 dark:text-white"
</script>

<Table {columns} items={objects} {labels} rowHeightInPx={36} {spans}>
  <svelte:fragment let:fieldName let:obj slot="field">
    {#if fieldName === "id" && linkDraftVersion}
      <DisplayField
        fieldname="id"
        value={obj.id}
        {wrapperClass}
        {valueClass}
        {model}
        extras={{ objectVersion: obj.draft_version_id }}
      />
    {:else}
      <DisplayField
        value={obj[fieldName]}
        fieldname={fieldName}
        {model}
        {wrapperClass}
        {valueClass}
      />
    {/if}
  </svelte:fragment>
</Table>
