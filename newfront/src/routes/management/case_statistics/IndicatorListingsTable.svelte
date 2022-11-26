<script lang="ts">
  import { formfields } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table from "$components/Table/Table.svelte"

  export let objects: Array<Deal | Investor> = []
  export let model: "deal" | "investor" = "deal"

  const dealColumns = {
    id: 1,
    country: 2,
    deal_size: 2,
    confidential: 2,
    created_at: 2,
    modified_at: 2,
    fully_updated_at: 3,
  }

  const investorColumns = {
    id: 1,
    name: 3,
    country: 4,
    created_at: 2,
    modified_at: 2,
  }

  $: columnsWithSpan = model === "deal" ? dealColumns : investorColumns
  $: columns = Object.keys(columnsWithSpan)
  $: labels = columns.map(col => $formfields?.[model]?.[col]?.label)
  $: spans = Object.entries(columnsWithSpan).map(([, colSpan]) => colSpan)
</script>

<Table {columns} items={objects} {labels} {spans}>
  <DisplayField
    fieldname={fieldName}
    let:fieldName
    let:obj
    {model}
    objectVersion={obj.current_draft_id}
    slot="field"
    value={obj[fieldName]}
    valueClasses=""
    wrapperClasses=""
  />
</Table>
