<script module lang="ts">
  // TODO: add parameter types for case_statistics endpoint and rename to data-statistics
  interface BaseObject {
    id: number
    status: string | null
    active_version_id: number | null
    draft_version_id: number | null
    draft_version__status: string | null

    country_id: number | null
    region_id: number | null

    created_at: string
    modified_at: string | null
  }

  export interface CaseStatisticsDeal extends BaseObject {
    fully_updated_at: string | null
    confidential: boolean
    deal_size: number | null
    active_version__is_public: boolean
    active_version__fully_updated: boolean
  }
  export interface CaseStatisticsInvestor extends BaseObject {
    name: string
  }
  export type CaseStatisticsObject = CaseStatisticsDeal | CaseStatisticsInvestor
</script>

<script lang="ts">
  import { dealFields, investorFields } from "$lib/fieldLookups"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table, { type Column } from "$components/Table/Table.svelte"

  interface Props {
    objects?: CaseStatisticsObject[]
    model?: "deal" | "investor"
    linkDraftVersion?: boolean
  }

  let { objects = [], model = "deal", linkDraftVersion = false }: Props = $props()

  let dealColumns: Column[] = $derived(
    [
      { key: "id", colSpan: 1 },
      { key: "status", colSpan: 2 },
      { key: "country_id", colSpan: 2 },
      { key: "deal_size", colSpan: 2 },
      { key: "confidential", colSpan: 2 },
      { key: "created_at", colSpan: 2 },
      { key: "modified_at", colSpan: 2 },
      { key: "fully_updated_at", colSpan: 3 },
    ].map(c => ({ ...c, label: $dealFields[c.key].label })),
  )

  let investorColumns: Column[] = $derived(
    [
      { key: "id", colSpan: 1 },
      { key: "status", colSpan: 2 },
      { key: "name", colSpan: 5 },
      { key: "country_id", colSpan: 4 },
      { key: "created_at", colSpan: 2 },
      { key: "modified_at", colSpan: 2 },
    ].map(c => ({ ...c, label: $investorFields[c.key].label })),
  )

  let columns = $derived(model === "deal" ? dealColumns : investorColumns)

  const wrapperClass = ""
  const valueClass = "text-gray-700 dark:text-white"
</script>

<div class="h-full w-full">
  <Table {columns} items={objects} rowHeightInPx={36}>
    {#snippet field({ fieldName, obj })}
      {@const col = columns.find(c => c.key === fieldName)}
      {#if col}
        <DisplayField
          fieldname={col.key}
          value={col.submodel ? obj[col.submodel][col.key] : obj[col.key]}
          {model}
          {wrapperClass}
          {valueClass}
          extras={col.key === "id" && linkDraftVersion
            ? { objectVersion: obj.draft_version_id }
            : undefined}
        />
      {/if}
    {/snippet}
  </Table>
</div>
