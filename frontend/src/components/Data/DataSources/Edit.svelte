<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealVersion2, InvestorVersion2 } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import { createDataSource, isEmptyDataSource } from "./dataSources"
  import Entry from "./Entry.svelte"

  interface Props {
    version: DealVersion2 | InvestorVersion2
  }

  let { version = $bindable() }: Props = $props()

  let datasources = $state(version.datasources)

  const onchange = () => {
    version.datasources = datasources
  }
</script>

<SubmodelEditField
  label={$_("Data Source")}
  bind:entries={datasources}
  createEntry={createDataSource}
  isEmpty={isEmptyDataSource}
  entryComponent={Entry}
  {onchange}
/>
