<script lang="ts">
  import { _ } from "svelte-i18n"

  import { DataSource, type DealHull } from "$lib/types/newtypes"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import Entry from "./Entry.svelte"

  export let deal: DealHull

  $: label = $_("Data Source")

  const createEntry = (nid: string) => new DataSource(nid)
</script>

<SubmodelEditField
  bind:entries={deal.selected_version.datasources}
  entryComponent={Entry}
  {createEntry}
  {label}
/>
