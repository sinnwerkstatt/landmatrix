<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealVersion2, InvestorVersion2 } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import { createDataSource, isEmptyDataSource } from "./dataSources"
  import Entry from "./Entry.svelte"

  export let version: DealVersion2 | InvestorVersion2
</script>

<SubmodelEditField
  label={$_("Data Source")}
  bind:entries={version.datasources}
  createEntry={createDataSource}
  isEmpty={isEmptyDataSource}
  entryComponent={Entry}
/>
