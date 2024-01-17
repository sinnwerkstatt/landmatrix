<script lang="ts">
  import { _ } from "svelte-i18n"

  import { formfields } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"

  import BooleanField from "$components/Fields/Display2/BooleanField.svelte"
  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"
  import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
  import IDField from "$components/Fields/Display2/IDField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"
  import Table from "$components/Table/Table.svelte"

  export let objects: Array<Deal | Investor> = []
  export let model: "deal" | "investor" = "deal"

  interface Col {
    key: string
    label: string
    colSpan: number
  }
  const dealColumns: Col[] = [
    { key: "id", label: $_("ID"), colSpan: 1 },
    { key: "mode", label: $_("Mode"), colSpan: 2 },
    { key: "country", label: $_("Target country"), colSpan: 2 },
    { key: "deal_size", label: $_("Deal size"), colSpan: 2 },
    { key: "confidential", label: $_("Confidential"), colSpan: 2 },
    { key: "created_at", label: $_("Created at"), colSpan: 2 },
    { key: "modified_at", label: $_("Last update"), colSpan: 2 },
    { key: "fully_updated_at", label: $_("Last full update"), colSpan: 3 },
  ]
  ;("Country of registration/origin")
  const investorColumns: Col[] = [
    { key: "id", label: $_("ID"), colSpan: 1 },
    { key: "mode", label: $_("Mode"), colSpan: 2 },
    { key: "name", label: $_("Name"), colSpan: 5 },
    { key: "country", label: $_("Target country"), colSpan: 4 },

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

<Table {columns} items={objects} {labels} {spans} rowHeightInPx={36}>
  <svelte:fragment slot="field" let:fieldName let:obj>
    {#if fieldName === "id"}
      <IDField fieldname="id" value={obj.id} {wrapperClass} {valueClass} {model} />
    {:else if fieldName === "mode"}
      {obj.mode}
    {:else if fieldName === "name"}
      <TextField
        fieldname="name"
        value={obj.active_version__name}
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "country"}
      <CountryField
        fieldname="country"
        value={obj.country_id}
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "deal_size"}
      <DecimalField
        value={obj.active_version__deal_size}
        fieldname="deal_size"
        unit={$_("ha")}
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "confidential"}
      <BooleanField
        value={obj.confidential}
        fieldname="confidential"
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "created_at"}
      <DateTimeField
        value={obj.first_created_at}
        fieldname="created_at"
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "modified_at"}
      <DateTimeField
        value={obj.active_version__modified_at}
        fieldname="modified_at"
        {wrapperClass}
        {valueClass}
      />
    {:else if fieldName === "fully_updated_at"}
      <DateTimeField
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
