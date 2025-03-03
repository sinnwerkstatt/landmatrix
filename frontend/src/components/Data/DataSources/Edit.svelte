<script lang="ts">
  import { _ } from "svelte-i18n"

  import type {
    DataSource,
    DealVersion2,
    InvestorVersion2,
    Model,
    Mutable,
  } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import { createDataSource, isEmptyDataSource } from "./dataSources"
  import Entry from "./Entry.svelte"

  interface Props {
    model: Model
    version: Mutable<DealVersion2> | Mutable<InvestorVersion2>
  }

  let { version = $bindable(), model }: Props = $props()

  // FIXME: Types
  let datasources = $state(version.datasources) as DataSource[]

  const onchange = () => {
    version = { ...version, datasources: datasources as never }
  }
</script>

<SubmodelEditField
  {model}
  fieldname="datasources"
  label={$_("Data Source")}
  bind:entries={datasources}
  createEntry={createDataSource}
  isEmpty={isEmptyDataSource}
  entryComponent={Entry}
  {onchange}
/>
