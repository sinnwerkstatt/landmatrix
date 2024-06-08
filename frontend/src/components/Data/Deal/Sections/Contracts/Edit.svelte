<script lang="ts">
  import { _ } from "svelte-i18n"

  import { Contract, type DealHull } from "$lib/types/newtypes"

  import JSONArrayField from "../../../../Fields/SubmodelEditField.svelte"
  import Entry from "./Entry.svelte"

  export let deal: DealHull

  $: label = $_("Contract")
</script>

<JSONArrayField
  bind:entries={deal.selected_version.contracts}
  createEntry={nid => new Contract(nid)}
  entryComponent={Entry}
  {label}
/>
