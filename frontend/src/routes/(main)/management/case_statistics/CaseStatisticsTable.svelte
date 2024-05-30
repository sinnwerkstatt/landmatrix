<script lang="ts">
  import { dealFields, investorFields } from "$lib/fieldLookups.js"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table, { type Column } from "$components/Table/Table.svelte"

  import type { CaseStatisticsDeal, CaseStatisticsInvestor } from "./caseStatistics"

  export let objects: Array<CaseStatisticsDeal | CaseStatisticsInvestor> = []
  export let model: "deal" | "investor" = "deal"
  export let linkDraftVersion = false

  let dealColumns: Column[]
  $: dealColumns = [
    { key: "id", colSpan: 1 },
    { key: "status", colSpan: 2 },
    { key: "country_id", colSpan: 2 },
    { key: "deal_size", colSpan: 2 },
    { key: "confidential", colSpan: 2 },
    { key: "created_at", colSpan: 2 },
    { key: "modified_at", colSpan: 2 },
    { key: "fully_updated_at", colSpan: 3 },
  ].map(c => ({ ...c, label: $dealFields[c.key].label }))

  let investorColumns: Column[]
  $: investorColumns = [
    { key: "id", colSpan: 1 },
    { key: "status", colSpan: 2 },
    { key: "name", colSpan: 5 },
    { key: "country_id", colSpan: 4 },
    { key: "created_at", colSpan: 2 },
    { key: "modified_at", colSpan: 2 },
  ].map(c => ({ ...c, label: $investorFields[c.key].label }))

  $: columns = model === "deal" ? dealColumns : investorColumns

  const wrapperClass = ""
  const valueClass = "text-gray-700 dark:text-white"
</script>

<Table {columns} items={objects} rowHeightInPx={36}>
  <svelte:fragment let:fieldName let:obj slot="field">
    {@const col = columns.find(c => c.key === fieldName)}
    <DisplayField
      fieldname={col.key}
      value={col.submodel ? obj[col.submodel][col.key] : obj[col.key]}
      {model}
      {wrapperClass}
      {valueClass}
      extras={col.key === "id" && linkDraftVersion
        ? { objectVersion: obj.draft_version_id }
        : {}}
    />
  </svelte:fragment>
</Table>
