<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import { createContract, isEmptyContract } from "./contracts"
  import Entry from "./Entry.svelte"

  export let deal: DealHull
</script>

<SubmodelEditField
  label={$_("Contract")}
  bind:entries={deal.selected_version.contracts}
  createEntry={createContract}
  isEmpty={isEmptyContract}
  entryComponent={Entry}
/>
